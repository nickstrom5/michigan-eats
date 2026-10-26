import SwiftUI

struct AboutView: View {
    @Environment(AppModel.self) private var model

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 8) {
                    Text("MICHIGAN EATS").displayFont(32).foregroundStyle(Theme.green)
                    Text("A free guide to \(model.restaurantCount.formatted()) Michigan restaurants, checked against the state's list of licensed food-service establishments, with hand-checked lists of Michigan's own food (coney islands, Detroit-style pizza, pasties, pączki, Middle Eastern kitchens, fish fries and supper clubs, the oldest places), James Beard honors, and the Detroit Health Department's own inspection results. No account, no ads, no tracking.")
                        .font(.subheadline).foregroundStyle(Theme.ink2)
                    Text("Michigan Eats (\u{201C}MI Eats\u{201D}) is an independent app by Nicholas Soderstrom. It is not affiliated with, endorsed by or operated by the State of Michigan, the Michigan Department of Agriculture and Rural Development, the Michigan Liquor Control Commission, any local health department, the City of Detroit, the Detroit Health Department, the James Beard Foundation, Apple, or any restaurant or chain. Other names are trademarks of their owners.")
                        .font(.footnote).foregroundStyle(Theme.muted)
                }
                .padding(.vertical, 4)
            }
            Section("How the lists are built") {
                Text("The coney island, Detroit-style pizza, pasty, pączki, Middle Eastern, fish fry and oldest-places lists are hand-checked: each place was checked against a 2025 or 2026 source (the place's own website or menu, local news or an official tourism listing), with the address checked. Founding years mean the year it opened at this address.")
                Text("Honors are James Beard Foundation awards and nominations from 2025 and 2026, plus America's Classics. Michigan has no MICHELIN Guide.")
                Text("Places start from open map listings (Overture Maps), checked against MDARD's statewide list of the food service establishments Michigan's local health departments license. Listings that matched an active license are marked official; of the rest, the app keeps the kinds that proved reliable (high-confidence listings matched a license \(rate("meta_high")) of the time). Licensed places the map data missed are added when their name says they're a place to eat. Adult clubs are left out. Website links are checked, and any that no longer belong to the place are left out.")
                Text("Inspection results are Detroit's own: the result of each routine inspection, in compliance or not, with the Priority, Priority Foundation and Core violations it cited. The other health departments don't publish results in bulk, and Michigan has no statewide grade, so this app computes none.")
                Text("Ratings, reviews, hours and photos are Apple Maps' own, shown live in Apple's place card. This app doesn't store or rank by them.")
            }
            .font(.subheadline).foregroundStyle(Theme.ink2)
            Section("Sources") {
                source("Michigan Department of Agriculture and Rural Development", "Michigan Restaurants and Commissaries (MDARD and Michigan's local health departments), active food service licenses read \(DayFormat.text(model.licensesUpdated) ?? ""), modified for use in this app. MDARD's terms: \u{201C}This Information is provided \u{2018}AS IS\u{2019} and on an \u{2018}AS AVAILABLE\u{2019} basis. The State of Michigan (\u{2018}State\u{2019}) makes no warranties, express or implied, regarding the accuracy, adequacy, reliability, timeliness, or completeness of this Information.\u{201D} For a license's official status, ask the local health department.", Links.mdardData.absoluteString)
                source("Detroit Health Department", "Restaurant Inspections (data.detroitmi.gov): routine inspections and the City's own results, through \(DayFormat.text(model.inspectionsThrough["det"]) ?? ""). The City publishes about a month late.", Links.detroitInspections.absoluteString)
                source("City of Detroit", "Liquor Licenses (data.detroitmi.gov), the City's monthly copy of the Michigan Liquor Control Commission list for Detroit, read \(DayFormat.text(model.liquorUpdated) ?? model.liquorUpdated).", Links.detroitLiquor.absoluteString)
                source("Overture Maps Foundation", "Restaurant listings and websites come from Overture Maps Foundation places data (overturemaps.org)\(model.overtureRelease.map { ", release \($0)" } ?? ""), filtered and reformatted for this app.\n• Data from Meta, Microsoft, DAC and BrightQuery. Available under CDLA Permissive 2.0.\n• Data from Foursquare. \(foursquareCopyright) Available under Apache 2.0. Foursquare data was transformed to the Overture schema; this app further filtered and reformatted it. See the NOTICE below.\n• Data from AllThePlaces. Available under CC0 1.0.", "https://overturemaps.org")
                source("Honors", "James Beard Foundation awards, finalists and America's Classics are reported as facts and checked by hand against the official announcements. James Beard Foundation and James Beard Award are trademarks of the James Beard Foundation. Other names belong to their owners.", "https://www.jamesbeard.org/awards")
                source("Maps", "Maps, place cards and directions by Apple Maps.", nil)
            }
            Section("Licenses") {
                NavigationLink("Community Data License Agreement – Permissive 2.0") { LicenseText(file: "CDLA-Permissive-2.0", title: "CDLA Permissive 2.0") }
                NavigationLink("Apache License 2.0") { LicenseText(file: "Apache-2.0", title: "Apache License 2.0") }
                NavigationLink("Foursquare OS Places NOTICE") { LicenseText(file: "Foursquare-NOTICE", title: "Foursquare NOTICE") }
            }
            Section("Privacy") {
                Text("The app collects nothing. Your location, if you allow it, only sorts lists by distance and shows where you are on the map, on this device. Saved places stay on this device.")
                    .font(.subheadline).foregroundStyle(Theme.ink2)
                DataUpdatesNote()
                    .font(.footnote).foregroundStyle(Theme.muted)
                Link("Privacy policy", destination: Links.privacy)
                Link("Terms of use", destination: Links.terms)
            }
            Section("Help") {
                Link("Report a missing or closed place", destination: Links.correctionEmail)
                Link("Email \(Links.supportEmail)", destination: URL(string: "mailto:\(Links.supportEmail)")!)
                Link("Website", destination: Links.site)
                Text("Data as of \(DayFormat.text(model.generated) ?? model.generated). Places open and close; check before you go. Version \(Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "1.0")")
                    .font(.footnote).foregroundStyle(Theme.muted)
            }
        }
        .navigationTitle("About")
        .tint(Theme.green)
    }

    /// the copyright line exactly as the bundled Foursquare NOTICE has it, so the two can't disagree
    private var foursquareCopyright: String {
        guard let url = Bundle.main.url(forResource: "Foursquare-NOTICE", withExtension: "txt"),
              let text = try? String(contentsOf: url, encoding: .utf8),
              let line = text.split(separator: "\n").first(where: { $0.hasPrefix("©") }) else { return "© Foursquare Labs, Inc. All rights reserved." }
        return line.trimmingCharacters(in: .whitespaces)
    }

    private func rate(_ group: String) -> String {
        let v = model.calibration.areas.values.compactMap { $0.groups[group]?.official }.map { Int(($0 * 100).rounded()) }.sorted()
        guard let lo = v.first, let hi = v.last else { return "most" }
        return lo == hi ? "\(lo)%" : "\(lo)–\(hi)%"
    }

    @ViewBuilder
    private func source(_ name: String, _ detail: String, _ url: String?) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            if let url, let u = URL(string: url) { Link(name, destination: u).font(.subheadline.weight(.semibold)) }
            else { Text(name).font(.subheadline.weight(.semibold)) }
            Text(detail).font(.caption).foregroundStyle(Theme.muted)
        }
    }
}

/// A bundled license text (Resources/Licenses), reflowed rather than shown as raw 80-column lines.
struct LicenseText: View {
    let file: String
    let title: String

    var body: some View {
        ScrollView {
            Text(text).font(.footnote).foregroundStyle(Theme.ink).textSelection(.enabled)
                .frame(maxWidth: .infinity, alignment: .leading).padding()
        }
        .inlineTitle(title)
    }

    private var text: String {
        guard let url = Bundle.main.url(forResource: file, withExtension: "txt"),
              let raw = try? String(contentsOf: url, encoding: .utf8) else { return "License text missing." }
        // join hard-wrapped lines into paragraphs; keep blank lines and list items as breaks
        var out: [String] = []
        for para in raw.components(separatedBy: "\n\n") {
            let lines = para.components(separatedBy: "\n").map { $0.trimmingCharacters(in: .whitespaces) }
            var joined = ""
            for l in lines where !l.isEmpty {
                let startsItem = l.hasPrefix("–") || l.hasPrefix("-") || l.range(of: #"^\(?[a-z0-9]{1,3}[.)]\s"#, options: .regularExpression) != nil
                joined += joined.isEmpty ? l : (startsItem ? "\n" + l : " " + l)
            }
            if !joined.isEmpty { out.append(joined) }
        }
        return out.joined(separator: "\n\n")
    }
}
