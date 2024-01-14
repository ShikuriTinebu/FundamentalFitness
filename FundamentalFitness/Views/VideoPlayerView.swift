//
//  VideoPlayerView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/12/24.
//

import AVKit
import SwiftUI

struct VideoPlayerView: View {
    let url = URL(string: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4")!
    
    var body: some View{
        NavigationView{
            VStack {
                VideoPlayer(
                    player: AVPlayer(url: url)
                ).scaledToFit()
            }
        }
    }
    
}
#Preview {
    VideoPlayerView() as! any View
}
