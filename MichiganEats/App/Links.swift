import Foundation

/// The app's web pages and support address, in one place.
/// The site is GitHub Pages at the project address until michigan.eatsranked.com resolves (Nick adds a Cloudflare CNAME
/// michigan -> nickstrom5.github.io, DNS only; then scripts/make-site.py sets CUSTOM_DOMAIN). GitHub forwards these github.io
/// links to the custom domain after the switch, so a shipped build keeps working; point them at the new domain in the next update.
enum Links {
    static let site = URL(string: "https://nickstrom5.github.io/michigan-eats/")!
    /// The app's data updates: scripts/publish_app_data.py writes docs/data/app/ (OTA-DATA.md).
    static let appData = URL(string: site.absoluteString + "data/app/")!
    static let privacy = URL(string: "https://nickstrom5.github.io/michigan-eats/privacy.html")!
    static let terms = URL(string: "https://nickstrom5.github.io/michigan-eats/terms.html")!
    /// MDARD's open list of the food service establishments Michigan's local health departments license (pages that open; checked with curl)
    static let mdardData = URL(string: "https://www.arcgis.com/home/item.html?id=f6232e1305d444f7a649b5defaa5f861")!
    /// the Detroit Health Department's inspections and the City's copy of the state liquor list
    static let detroitInspections = URL(string: "https://data.detroitmi.gov/datasets/restaurant-inspections")!
    static let detroitLiquor = URL(string: "https://data.detroitmi.gov/datasets/liquor-licenses")!
    static let supportEmail = "nick@eatsranked.com"

    static var correctionEmail: URL {
        URL(string: "mailto:\(supportEmail)?subject=Michigan%20Eats%20correction")!
    }
}
