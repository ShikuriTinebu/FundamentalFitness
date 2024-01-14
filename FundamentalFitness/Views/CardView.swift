//
//  CardView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct CardView: View {
    var musclesUsed: String
    var exerciseTitle: String
    var imageName: String
    
    var body: some View {
        VStack{
            Image(imageName).resizable().aspectRatio(contentMode: .fit)
            
            HStack{
                VStack(alignment: .leading) {
                    Text(musclesUsed)
                        .font(.headline)
                        .foregroundColor(.secondary)
                    Text(exerciseTitle)
                        .font(.title)
                        .fontWeight(.black)
                        .foregroundColor(.primary)
                        .lineLimit(3)
                    //Text("".uppercased())
                        .font(.caption)
                        .foregroundColor(.secondary)
                }.layoutPriority(100)
                Spacer()
            }.padding()
        }.cornerRadius(10).overlay(
            RoundedRectangle(cornerRadius: 10)
                .stroke(Color.white, lineWidth: 1)
        )
        .padding([.top, .horizontal])
 
        
    }
}

#Preview {
    CardView(musclesUsed: "Legs", exerciseTitle: "Running", imageName: "runningimage")
}
