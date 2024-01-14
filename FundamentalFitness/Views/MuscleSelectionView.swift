//
//  MuscleSelectionView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct MuscleSelectionView: View {
    @State private var chestSelected = false;
    @State private var backSelected = false;
    @State private var absSelected = false;
    @State private var legsSelected = false;
    @State private var armsSelected = false;
    
    
    var body: some View {
    
        VStack(spacing: 30){
            
            Text("Choose your focus areas").foregroundColor(.white).fontWeight(.bold).font(Font.system(size: 27))
            
            VStack{
                SelectButton(isSelected: $chestSelected, color: .blue, text: "Chest").frame(width: 350).onTapGesture {
                    chestSelected.toggle()
                }
                SelectButton(isSelected: $backSelected, color: .blue, text: "Back").frame(width: 350).onTapGesture {
                    backSelected.toggle()
                }
                SelectButton(isSelected: $absSelected, color: .blue, text: "Abs").frame(width: 350).onTapGesture {
                    absSelected.toggle()
                }
                SelectButton(isSelected: $legsSelected, color: .blue, text: "Legs").frame(width: 350).onTapGesture {
                    legsSelected.toggle()
                }
                SelectButton(isSelected: $armsSelected, color: .blue, text: "Arms").frame(width: 350).onTapGesture {
                    armsSelected.toggle()
                }
                Spacer()
                NavigationLink("CONTINUE", destination: MainView()).frame(width: 350, height: 60).background(.blue).cornerRadius(15).foregroundColor(.white).fontWeight(.bold).font(.headline).padding()
            }
            
        }.padding()
        
    }
}

#Preview {
    MuscleSelectionView()
}
