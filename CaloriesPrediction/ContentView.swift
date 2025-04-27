import SwiftUI
import CoreML
import HealthKit

struct ContentView: View {
    @StateObject private var healthManager = HealthManager()

    @State private var gender = "male"
    @State private var age = ""
    @State private var height = ""
    @State private var weight = ""
    @State private var duration = ""
    @State private var heartRate = ""
    @State private var bodyTemp = "36.5"
    @State private var prediction = "-"

    let genderOptions = ["male", "female"]

    var body: some View {
        VStack(spacing: 20) {
            Text("Calorie Burn Predictor")
                .font(.title2)
                .bold()

            Picker("Gender", selection: $gender) {
                ForEach(genderOptions, id: \.self) { Text($0) }
            }
            .pickerStyle(SegmentedPickerStyle())

            TextField("Age", text: $age).keyboardType(.numberPad)

            Group {
                TextField("Height (cm)", text: $height)
                    .keyboardType(.decimalPad)
                    .onChange(of: healthManager.latestHeight) {
                        if let v = healthManager.latestHeight {
                            height = String(format: "%.1f", v)
                        }
                    }

                TextField("Weight (kg)", text: $weight)
                    .keyboardType(.decimalPad)
                    .onChange(of: healthManager.latestHeight) {
                        if let v = healthManager.latestHeight {
                            weight = String(format: "%.1f", v)
                        }
                    }

                TextField("Duration (min)", text: $duration)
                    .keyboardType(.decimalPad)
                    .onChange(of: healthManager.latestDuration) {
                        if let v = healthManager.latestDuration {
                            duration = String(format: "%.1f", v)
                        }
                    }

                TextField("Heart Rate (bpm)", text: $heartRate)
                    .keyboardType(.decimalPad)
                    .onChange(of: healthManager.latestHeartRate) {
                        if let v = healthManager.latestHeartRate {
                            heartRate = String(format: "%.0f", v)
                        }
                    }
                

                TextField("Body Temp (°C)", text: $bodyTemp)
                    .keyboardType(.decimalPad)
                    .onChange(of: healthManager.latestBodyTemp) {
                        if let v = healthManager.latestBodyTemp {
                            bodyTemp = String(format: "%.1f", v)
                        }
                    }
            }

            HStack {
                Button("Fetch from Watch") {
                    healthManager.requestAuthorization()
                }

                Button("Predict Calories") {
                    predictCalories()
                }
            }
            .padding(.top, 10)

            Text("Prediction: \(prediction) kcal")
                .font(.title3)
                .padding()
        }
        .padding()
    }

    func predictCalories() {
        guard let ageVal = Double(age),
              let heightVal = Double(height),
              let weightVal = Double(weight),
              let durationVal = Double(duration),
              let heartRateVal = Double(heartRate),
              let bodyTempVal = Double(bodyTemp) else {
            prediction = "Missing or invalid input"
            return
        }

        let genderVal: Double = (gender.lowercased() == "male") ? 0 : 1

        do {
            let model = try CaloriesPredictorFromCSV(configuration: .init())
            let result = try model.prediction(
                Gender: genderVal,
                Age: ageVal,
                Height: heightVal,
                Weight: weightVal,
                Duration: durationVal,
                Heart_Rate: heartRateVal,
                Body_Temp: bodyTempVal
            )

            if let outputKey = result.featureNames.first,
               let calories = result.featureValue(for: outputKey)?.doubleValue {
                prediction = String(format: "%.1f", calories)
            } else {
                prediction = "No output"
            }
        } catch {
            print("Prediction failed: \(error)")
            prediction = "Error"
        }
    }
}
