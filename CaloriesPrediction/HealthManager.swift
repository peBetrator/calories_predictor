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
        fetchQuantity(.heartRate) { self.latestHeartRate = $0 }
        fetchQuantity(.bodyTemperature) { self.latestBodyTemp = $0 }
        fetchWorkoutDuration()
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
}
