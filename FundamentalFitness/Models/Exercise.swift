//
//  Exercise.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/12/24.
//

import Foundation
import SwiftUI

struct Exercise: Hashable, Codable, Identifiable{
    var id: Int
    var name: String
    var muscleUsed: String
    var imageName: String
    var image: Image {
        Image(imageName)
    }
    
    init(id: Int, name: String, imageName: String, muscleUsed: String) {
        self.id = id
        self.name = name
        self.imageName = imageName
        self.muscleUsed = muscleUsed
    }
    
    
}


