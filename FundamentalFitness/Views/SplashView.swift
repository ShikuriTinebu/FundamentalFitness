//
//  SplashView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/13/24.
//

import SwiftUI

struct SplashView: View {
    var body: some View {
        ZStack{
            Rectangle().background(Color.white)
            VStack{
                Image("applogo").resizable().scaledToFit().frame(width: 300, height: 300)
                Text("Fundamental Fitness").foregroundColor(.white).font(.title)
            }
        }
    }
}

#Preview {
    SplashView()
}
