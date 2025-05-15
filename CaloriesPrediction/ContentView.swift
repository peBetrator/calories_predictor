import SwiftUI
import CoreML
import HealthKit

struct ContentView: View {
    @StateObject private var healthManager = HealthManager()

    @State private var gender = "male"
    @AppStorage("selectedAge") private var selectedAge: Int = 25
    @State private var isAgePickerPresented = false

    @State private var height = ""
    @State private var weight = ""
    @State private var duration = ""
    @State private var heartRate = ""
    @State private var bodyTemp = "37.5"
    @State private var prediction = "-"
    
    @State private var showFireEffect = false
    @State private var showPrediction = false

    let genderOptions = ["male", "female"]

    var body: some View {
        ZStack {
            VStack(spacing: 20) {
                Text("Calories Burn Predictor")
                    .font(.title2)
                    .bold()

                Picker("Gender", selection: $gender) {
                    ForEach(genderOptions, id: \.self) { Text($0) }
                }
                .pickerStyle(SegmentedPickerStyle())

                // Age Input (Styled Like Button)
                Button(action: { isAgePickerPresented = true }) {
                    HStack {
                        Text("Age")
                        Spacer()
                        Text("\(selectedAge)")
                            .foregroundColor(.primary)
                    }
                    .padding()
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.gray.opacity(0.5), lineWidth: 1)
                    )
                }
                .sheet(isPresented: $isAgePickerPresented) {
                    VStack {
                        Text("Select Age")
                            .font(.headline)
                            .padding()

                        Picker("Age", selection: $selectedAge) {
                            ForEach(1...120, id: \.self) { age in
                                Text("\(age)").tag(age)
                            }
                        }
                        .pickerStyle(WheelPickerStyle())
                        .labelsHidden()

                        Button("Done") {
                            isAgePickerPresented = false
                        }
                        .padding()
                    }
                    .presentationDetents([.fraction(0.4)])
                }

                // Styled Numeric Inputs
                inputField(label: "Height (cm)", binding: $height, value: healthManager.latestHeight, format: "%.0f")
                inputField(label: "Weight (kg)", binding: $weight, value: healthManager.latestWeight, format: "%.1f")
                inputField(label: "Duration (min)", binding: $duration, value: healthManager.latestDuration, format: "%.0f")
                inputField(label: "Heart Rate (bpm)", binding: $heartRate, value: healthManager.latestHeartRate, format: "%.0f")
                inputField(label: "Body Temp (°C)", binding: $bodyTemp, value: healthManager.latestBodyTemp, format: "%.1f")

                HStack {
                    Button("Fetch from Watch") {
                        healthManager.requestAuthorization()
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.large)
                    .frame(maxWidth: .infinity)
                    .clipShape(RoundedRectangle(cornerRadius: 12))

                    Button("Predict Calories") {
                        showFireEffect = true
                        showPrediction = false

                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.7) {
                            showFireEffect = false
                            showPrediction = true
                            predictCalories()
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.green) // Optional: Change the color for action emphasis
                    .controlSize(.large)
                    .frame(maxWidth: .infinity)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                .padding(.top, 10)
                
                Group {
                    if showPrediction {
                        Text("Prediction: \(prediction) kcal")
                            .font(.title3)
                            .transition(.opacity)
                    } else {
                        Text(" ")
                            .font(.title3)
                            .opacity(0)
                    }
                }
                .frame(height: 40)
            }
            .padding()
            .onTapGesture {
                UIApplication.shared.endEditing()
            }
            if showFireEffect {
                FireEffectView()
                    .transition(.move(edge: .bottom))
                    .zIndex(2)
            }
        }
        .overlay(
            showFireEffect ? FireEffectView().zIndex(2) : nil
        )
    }

    // MARK: - Reusable Styled Input Field
    func inputField(label: String, binding: Binding<String>, value: Double?, format: String) -> some View {
        HStack {
            Text(label)
            Spacer()
            TextField("", text: binding)
                .multilineTextAlignment(.trailing)
                .keyboardType(.numbersAndPunctuation)
        }
        .padding()
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(Color.gray.opacity(0.5), lineWidth: 1)
        )
        .onChange(of: value) { newVal in
            if let v = newVal {
                binding.wrappedValue = String(format: format, v)
            }
        }
    }

    // MARK: - Prediction Logic
    func predictCalories() {
        guard let heightVal = Double(height),
              let weightVal = Double(weight),
              let durationVal = Double(duration),
              let heartRateVal = Double(heartRate),
              let bodyTempVal = Double(bodyTemp) else {
            prediction = "Missing or invalid input"
            return
        }

        let genderVal: Double = (gender.lowercased() == "male") ? 0 : 1
        let ageVal = Double(selectedAge)

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

extension UIApplication {
    func endEditing() {
        sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
}
