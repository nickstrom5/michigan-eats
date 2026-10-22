import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, coney, pizza, pasty, detail, map, honors, oldest, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // downtown Detroit (Campus Martius), so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 42.3315, longitude: -83.0466)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        // App Store rule: no screenshot shows a place whose latest Detroit result is "Not in compliance" (Lafayette's was, Jan 2026),
        // so the coney shots use American Coney Island (in compliance)
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("American Coney Island", "Detroit"), pick("Buddy's Pizza", "Detroit"), pick("Lehto's Pasties", "St. Ignace")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "coney": open(.coney)
        case "pizza": open(.detroitPizza)
        case "pasty":
            // from Marquette, so the nearest pasty shops are a short drive
            model.screenshotLocation = CLLocation(latitude: 46.5436, longitude: -87.3954)
            open(.pasty)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            open(.coney)
            if let p = pick("American Coney Island", "Detroit") ?? model.places.first { model.selectedPlace = p; model.guidesPath.append(.place(p)) }
        case "map": model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Buddy's Pizza", "Detroit")
        case "coney": pick("American Coney Island", "Detroit")
        case "pizza": pick("Buddy's Pizza", "Detroit")
        case "map": pick("American Coney Island", "Detroit")
        case "pasty": pick("Lehto's Pasties", "St. Ignace")
        case "saved", "oldest", "honors": pick("Lehto's Pasties", "St. Ignace")
        case "about": nil
        default: pick("American Coney Island", "Detroit")
        }
        model.selectedPlace = place
    }
}
