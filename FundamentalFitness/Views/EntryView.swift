//
//  EntryView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct EntryView: View {
    var body: some View {
        NavigationView{
            VStack{
                Image("FitnessLoadingScreen").resizable().aspectRatio(contentMode: .fit)
                ZStack{
                    NavigationLink("GET STARTED", destination: MuscleSelectionView()).frame(width: 350, height: 60).background(.blue).cornerRadius(15).foregroundColor(.white).fontWeight(.bold).font(.headline)

                }
            }
        }
    }
}

#Preview {
    EntryView()
}
