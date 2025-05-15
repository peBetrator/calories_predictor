import HealthKit
import Foundation

class HealthManager: ObservableObject {
    private var healthStore = HKHealthStore()

    @Published var latestHeight: Double?
    @Published var latestWeight: Double?
    @Published var latestHeartRate: Double?
    @Published var latestBodyTemp: Double?
    @Published var latestDuration: Double?

    func requestAuthorization() {
        guard HKHealthStore.isHealthDataAvailable() else { return }

        let readTypes: Set = [
            HKObjectType.quantityType(forIdentifier: .height)!,
            HKObjectType.quantityType(forIdentifier: .bodyMass)!,
            HKObjectType.quantityType(forIdentifier: .heartRate)!,
            HKObjectType.quantityType(forIdentifier: .bodyTemperature)!,
            HKObjectType.workoutType()
        ]

        healthStore.requestAuthorization(toShare: [], read: readTypes) { success, _ in
            if success {
                self.fetchAll()
            }
        }
    }

    func fetchAll() {
        fetchQuantity(.height) { self.latestHeight = $0 }
        fetchQuantity(.bodyMass) { self.latestWeight = $0 }
        fetchQuantity(.bodyTemperature) { self.latestBodyTemp = $0 }
        fetchWorkoutDuration()
        fetchLatestWorkoutHeartRate()
    }

    private func fetchQuantity(_ id: HKQuantityTypeIdentifier, completion: @escaping (Double?) -> Void) {
        guard let type = HKObjectType.quantityType(forIdentifier: id) else {
            completion(nil); return
        }

        let query = HKSampleQuery(sampleType: type, predicate: nil, limit: 1, sortDescriptors: [
            NSSortDescriptor(key: HKSampleSortIdentifierEndDate, ascending: false)
        ]) { _, samples, _ in
            guard let sample = samples?.first as? HKQuantitySample else {
                completion(nil); return
            }

            let unit: HKUnit = switch id {
            case .height: .meterUnit(with: .centi)
            case .bodyMass: .gramUnit(with: .kilo)
            case .heartRate: HKUnit.count().unitDivided(by: .minute())
            case .bodyTemperature: .degreeCelsius()
            default: .count()
            }

            completion(sample.quantity.doubleValue(for: unit))
        }

        healthStore.execute(query)
    }

    private func fetchWorkoutDuration() {
        let query = HKSampleQuery(sampleType: .workoutType(), predicate: nil, limit: 1, sortDescriptors: [
            NSSortDescriptor(key: HKSampleSortIdentifierEndDate, ascending: false)
        ]) { _, samples, _ in
            guard let workout = samples?.first as? HKWorkout else { return }
            self.latestDuration = workout.duration / 60  // seconds to minutes
        }

        healthStore.execute(query)
    }
    
    private func fetchLatestWorkoutHeartRate() {
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierEndDate, ascending: false)
        let workoutQuery = HKSampleQuery(sampleType: .workoutType(), predicate: nil, limit: 1, sortDescriptors: [sortDescriptor]) { _, samples, _ in
            guard let workout = samples?.first as? HKWorkout else { return }

            // Fetch heart rate samples during this workout
            guard let heartRateType = HKObjectType.quantityType(forIdentifier: .heartRate) else { return }

            let predicate = HKQuery.predicateForSamples(withStart: workout.startDate, end: workout.endDate, options: .strictStartDate)

            let heartRateQuery = HKSampleQuery(sampleType: heartRateType, predicate: predicate, limit: HKObjectQueryNoLimit, sortDescriptors: nil) { _, hrSamples, _ in
                guard let samples = hrSamples as? [HKQuantitySample], !samples.isEmpty else { return }

                let unit = HKUnit.count().unitDivided(by: .minute())
                let heartRates = samples.map { $0.quantity.doubleValue(for: unit) }
                let avgHeartRate = heartRates.reduce(0, +) / Double(heartRates.count)

                DispatchQueue.main.async {
                    self.latestHeartRate = avgHeartRate
                }
            }

            self.healthStore.execute(heartRateQuery)
        }

        healthStore.execute(workoutQuery)
    }
}
