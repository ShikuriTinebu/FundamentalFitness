//
//  MainView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct MainView: View {
    var body: some View {
        VStack{
            TabView{
                ExerciseListView(exerciseType: "Weights", exerciseList: weightExercises)
                    .tabItem {
                        Label("Weights", systemImage: "dumbbell")
                    }
                ExerciseListView(exerciseType: "Cardio", exerciseList: cardioExercises)
                    .tabItem {
                        Label("Cardio", systemImage: "figure.run")
                    }
                ExerciseListView(exerciseType: "Yoga", exerciseList: yogaExercises).tabItem {
                    Label("Yoga", systemImage: "figure.yoga")
                }
                Text("").tabItem {
                    Label("Calories", systemImage: "fork.knife")
                }
                
                PedometerView().tabItem {
                    Label("Steps", systemImage: "figure.walk")
                }
                
            }
        }
    }
}

#Preview {
    MainView()
}
