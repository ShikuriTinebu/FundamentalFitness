//
//  SelectButton.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct SelectButton: View {
    @Binding var isSelected: Bool
    @State var color: Color
    @State var text: String
    var body: some View {
        ZStack{
            Capsule().frame(height: 50).foregroundColor(isSelected ? color : .gray)
            Text(text).foregroundStyle(.white)
        }
    }
}

#Preview {
    SelectButton(isSelected: .constant(true), color: .gray, text: "Option")
}
