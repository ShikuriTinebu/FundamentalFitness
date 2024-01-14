//
//  ExerciseDetailView.swift
//  FundamentalFitness
//
//  Created by Sohom Dutta on 1/12/24.
//

import AVKit
import PhotosUI
import SwiftUI

struct Movie: Transferable {
    let url: URL

    static var transferRepresentation: some TransferRepresentation {
        FileRepresentation(contentType: .movie) { movie in
            SentTransferredFile(movie.url)
        } importing: { received in
            let copy = URL.documentsDirectory.appending(path: "movie.mp4")

            if FileManager.default.fileExists(atPath: copy.path()) {
                try FileManager.default.removeItem(at: copy)
            }

            try FileManager.default.copyItem(at: received.file, to: copy)
            return Self.init(url: copy)
        }
    }
}

struct ExerciseDetailView: View {
    enum LoadState {
        case unknown, loading, loaded(Movie), failed
    }

    @State private var selectedItem: PhotosPickerItem?
    @State private var loadState = LoadState.unknown
    @State private var selectedCriteria: Type = .instructions
    
    //private let neededEquipment =

    var body: some View {
        ScrollView {
            VideoPlayerView().scaledToFit().frame(width: 400, height: 300)
            PhotosPicker(selection: $selectedItem, matching: .videos){
                Text("Try it Yourself").padding().background(RoundedRectangle(cornerRadius: 10).stroke(.blue, lineWidth: 1))
            }
            Picker("Type", selection: $selectedCriteria){
                Text("Instructions").tag(Type.instructions)
                Text("Equipment").tag(Type.equipment)
            }.pickerStyle(.segmented).padding()
            
            switch selectedCriteria{
                case .equipment:
                    Text("Start by standing with your feet shoulder-width apart. Engage your core muscles and keep your chest up. Begin the movement by pushing your hips back as if you're sitting into a chair, while simultaneously bending your knees. Keep your back straight and lower your body down until your thighs are parallel to the ground or as far as your flexibility allows. Ensure that your knees are tracking over your toes and not extending beyond them. Press through your heels to return to the starting position, fully extending your hips and knees. Repeat the motion for a set number of repetitions, maintaining proper form throughout. Squats are a compound exercise that targets the muscles in your thighs, hips, and buttocks, and they can be incorporated into various fitness routines for strength and lower body development.").padding(30)
                case .instructions:
                    Text("Start by standing with your feet shoulder-width apart. Engage your core muscles and keep your chest up. Begin the movement by pushing your hips back as if you're sitting into a chair, while simultaneously bending your knees. Keep your back straight and lower your body down until your thighs are parallel to the ground or as far as your flexibility allows. Ensure that your knees are tracking over your toes and not extending beyond them. Press through your heels to return to the starting position, fully extending your hips and knees. Repeat the motion for a set number of repetitions, maintaining proper form throughout. Squats are a compound exercise that targets the muscles in your thighs, hips, and buttocks, and they can be incorporated into various fitness routines for strength and lower body development.").padding(30)
            }

            switch loadState {
            case .unknown:
                EmptyView()
            case .loading:
                ProgressView()
            case .loaded(let movie):
                VideoPlayer(player: AVPlayer(url: movie.url))
                        .scaledToFit()
                        .frame(width: 300, height: 300)
            case .failed:
                Text("Import failed")
            }
            
            Spacer()
        }
        .onChange(of: selectedItem) { _ in
            Task {
                do {
                    loadState = .loading

                    if let movie = try await selectedItem?.loadTransferable(type: Movie.self) {
                        loadState = .loaded(movie)
                    } else {
                        loadState = .failed
                    }
                } catch {
                    loadState = .failed
                }
            }
        }
    }
}

enum Type: String, CaseIterable, Identifiable{
    case instructions, equipment
    var id: Self { self }
}

#Preview {
    ExerciseDetailView()
}
