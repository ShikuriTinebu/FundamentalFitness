//
//  PedometerView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct PedometerView: View {
    @State private var healthStore = HealthStore()
    
    private var steps: [Step] {
        healthStore.steps.sorted{lhs, rhs in
            lhs.date > rhs.date
        }
    }
    
    var body: some View {
        VStack{
            if let step = steps.first {
                TodayStepView(step: step)
            }
            StepListView(steps: Array(steps.dropFirst()))
        }.task{
            await healthStore.requestAuthorization()
            do {
                try await healthStore.calculateSteps()
            } catch {
                print(error)
            }
        }.padding()
    }
}

#Preview {
    PedometerView()
}
