//
//  ListView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/12/24.
//

import SwiftUI

struct ExerciseListView: View {
    
    private let exerciseType: String
    private let exerciseList: [Exercise]
    init(exerciseType: String, exerciseList: [Exercise]){
        self.exerciseType = exerciseType
        self.exerciseList = exerciseList
    }
    
    var body: some View {
        //NavigationView{
            VStack{
                    
                List(exerciseList){ exercise in
                    
                    NavigationLink{
                        ExerciseDetailView()
                    } label: {
                        CardView(musclesUsed: exercise.muscleUsed, exerciseTitle: exercise.name, imageName: exercise.imageName)
                        //ExerciseRowView(exercise: exercise)
                    }
                }.listRowSeparator(.hidden)
                    //List(exerciseList, id: \.id){exercise in
                      //      ExerciseRowView(exercise: exercise)
                    //}
                    
            }.navigationTitle(exerciseType)

       //}
    }
}

#Preview {
    ExerciseListView(exerciseType: "Weights", exerciseList: weightExercises)
}
