import SwiftUI
import UIKit
import CoreText

/// Great Lakes palette (Nick's pick, 2026-10-22), light only: deep lake #0D3F63 (11.4:1 on white) for titles, tint and accents;
/// Northwoods pine #2E5E47 (7.3:1) for the hand-checked Michigan guide cards; Great Lakes blue #1B6EA8 (5.0:1) for links and the
/// water in the shoreline band; sand #E3D5AE for the beach line, fills only. No team or college colors (maize-and-blue vs
/// green-and-white splits the state). The names `green`/`gold`/`red` are kept from Wisconsin Eats so the shared views read the same:
/// here `green` is deep lake, `gold` and `red` the pine.
enum Theme {
    static let green = Color(hex: 0x0D3F63)      // deep lake: titles, tint, primary text accents
    static let green2 = Color(hex: 0x1B6EA8)     // Great Lakes blue
    static let gold = Color(hex: 0x2E5E47)       // pine: card fills under white text, chips
    static let goldSoft = Color(hex: 0xE1EEE7)
    static let lime = Color(hex: 0xE3D5AE)       // sand (the beach line), fills only
    static let limeSoft = Color(hex: 0xF4EEDC)
    static let sand = Color(hex: 0xF6F3EB)
    static let red = Color(hex: 0x2E5E47)        // pine: the Michigan guide cards and honors chips
    static let ink = Color(hex: 0x0C1D2A)
    static let ink2 = Color(hex: 0x24384A)
    static let muted = Color(hex: 0x536575)
    static let surface = Color.white
    static let surface2 = Color(hex: 0xF2F6F8)
    static let surface3 = Color(hex: 0xE1EAEF)
    static let rule = Color(hex: 0xDAE3EA)
    static let rule2 = Color(hex: 0xB3C4D0)
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// A small uppercase label: "STONE CRAB", "1 MICHELIN STAR".
struct Chip: View {
    enum Style { case gold, green, red, plain, dashed }
    let text: String
    var style: Style = .plain

    var body: some View {
        Text(text.uppercased())
            .font(.caption2.weight(.bold))
            .tracking(0.4)
            .padding(.horizontal, 7).padding(.vertical, 3)
            .foregroundStyle(style == .green || style == .red ? Color.white : style == .dashed ? Theme.muted : style == .gold ? Theme.ink : Theme.green)
            .background {
                RoundedRectangle(cornerRadius: 5).fill(style == .gold ? Theme.goldSoft : style == .green ? Theme.green : style == .red ? Theme.red
                                                       : style == .dashed ? .clear : Theme.surface2)
            }
            .overlay {
                if style == .dashed { RoundedRectangle(cornerRadius: 5).strokeBorder(Theme.rule2, style: StrokeStyle(lineWidth: 1, dash: [3, 2])) }
            }
            .accessibilityLabel(text)
    }
}

/// Detroit's own inspection result, as published: "Detroit · In compliance · 0 priority". Michigan has no statewide grade and the
/// app computes none.
struct BandBadge: View {
    let city: InspectionCity
    let band: InspectionBand
    var score: Int? = nil
    var large = false

    var body: some View {
        Text(([city.name, band.label] + (score.map { ["\($0) priority"] } ?? [])).joined(separator: " · ").uppercased())
            .font(large ? .footnote.weight(.heavy) : .caption2.weight(.heavy))
            .tracking(0.4)
            .multilineTextAlignment(.leading)
            .padding(.horizontal, large ? 10 : 7).padding(.vertical, large ? 6 : 3)
            .foregroundStyle(band.ink)
            .background(RoundedRectangle(cornerRadius: 6).fill(band.fill))
            .accessibilityLabel("\(city.name) inspection: \(band.label)" + (score.map { ", \($0) priority violations" } ?? ""))
    }
}

/// Michigan Eats' lettering: the system face drawn compressed and heavy for titles and guide names (like a lakeside diner sign), and the
/// system monospaced face for numbers, dates and small labels. No bundled fonts.
struct DisplayFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .black
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight).width(.compressed))
    }
}

/// Numbers, dates and small labels in the system monospaced face, scaled like DisplayFont.
struct MonoFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .semibold
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight, design: .monospaced))
    }
}

extension View {
    func displayFont(_ size: CGFloat, weight: Font.Weight = .black) -> some View {
        modifier(DisplayFont(size: size, weight: weight))
    }

    func monoFont(_ size: CGFloat, weight: Font.Weight = .semibold) -> some View {
        modifier(MonoFont(size: size, weight: weight))
    }
}

/// The Great Lakes shoreline band under the Home title (Nick's pick, 2026-10-22): deep lake, a sand beach line and lake-blue water
/// with one gentle swell, laid flat. No map, no team marks.
struct Stripes: View {
    var height: CGFloat = 6

    var body: some View {
        VStack(spacing: 0) {
            Rectangle().fill(Theme.green).frame(height: height * 1.4)
            Rectangle().fill(Theme.lime).frame(height: height * 0.8)
            Swell().fill(Theme.green2).frame(height: height * 1.2)
        }
        .clipShape(RoundedRectangle(cornerRadius: 3))
        .accessibilityHidden(true)
    }

    private struct Swell: Shape {
        func path(in r: CGRect) -> Path {
            var p = Path()
            p.move(to: CGPoint(x: r.minX, y: r.minY + r.height * 0.35))
            p.addCurve(to: CGPoint(x: r.maxX, y: r.minY + r.height * 0.35),
                       control1: CGPoint(x: r.minX + r.width * 0.33, y: r.minY - r.height * 0.1),
                       control2: CGPoint(x: r.minX + r.width * 0.66, y: r.minY + r.height * 0.8))
            p.addLine(to: CGPoint(x: r.maxX, y: r.maxY)); p.addLine(to: CGPoint(x: r.minX, y: r.maxY)); p.closeSubpath()
            return p
        }
    }
}

extension View {
    /// An inline navigation title in the display type. UINavigationBar.appearance() didn't reach every SwiftUI bar on iOS 27
    /// (the Map title went from compressed blue to plain black after a push and pop; place titles were always plain), so the
    /// title is our own view in the bar. The navigation title is still set, for the back button and VoiceOver.
    func inlineTitle(_ title: String) -> some View {
        navigationTitle(title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text(title).displayFont(19, weight: .heavy).foregroundStyle(Theme.green)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .accessibilityAddTraits(.isHeader)
                }
            }
    }
}
