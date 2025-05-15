import SwiftUI

struct FireEffectView: View {
    @State private var animateIn = false
    @State private var animateOut = false

    let appearDuration: Double = 0.8
    let holdDuration: Double = 0.1
    let disappearDuration: Double = 0.4

    var body: some View {
        GeometryReader { geometry in
            LinearGradient(
                colors: [.red, .orange, .yellow],
                startPoint: .bottom,
                endPoint: .top
            )
            .opacity(0.5)
            .frame(width: geometry.size.width, height: geometry.size.height)
            .mask(
                Rectangle()
                    .frame(
                        height: animateIn
                            ? (animateOut ? 0 : geometry.size.height + 500)
                            : 0,
                        alignment: .bottom
                    )
                    .frame(maxHeight: .infinity, alignment: .bottom) // ✅ Force align to bottom
                    .animation(
                        animateOut
                            ? .linear(duration: disappearDuration)
                            : .easeOut(duration: appearDuration),
                        value: animateIn
                    )
            )
            .ignoresSafeArea()
            .onAppear {
                animateIn = true
                DispatchQueue.main.asyncAfter(deadline: .now() + appearDuration + holdDuration) {
                    animateOut = true
                }
            }
        }
    }
}


