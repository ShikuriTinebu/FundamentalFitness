//
//  ExerciseRowView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/12/24.
//

import SwiftUI

struct ExerciseRowView: View {
    var exercise: Exercise
    var body: some View {
        
        VStack {
            HStack{
                exercise.image.resizable().frame(width: 60, height: 75)
                Text(exercise.name).padding(10)
                Spacer()
            }
        }.padding(5)
    }
}

#Preview {
    ExerciseRowView(exercise: weightExercises[0])
}
