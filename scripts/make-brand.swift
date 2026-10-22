// Michigan Eats brand: the app icon (Nick's pick 2026-10-22, concept A of scripts/icon-concepts.swift: a Detroit coney on deep lake),
// in the shared Eats Ranked style (../state-prompts/ICON-STYLE.md). Usage, from mi-eats/: swift scripts/make-brand.swift
// -> MichiganEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png, the website's icons (docs/icon-512.png, icon-192.png,
// apple-touch-icon.png, favicon-32.png) and share image (docs/og.png).
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let LAKE: UInt32 = 0x0D3F63

func rr(_ c: CGContext, _ r: CGRect, _ rad: CGFloat, _ hex: UInt32) {
    c.setFillColor(rgb(hex)); c.addPath(CGPath(roundedRect: r, cornerWidth: rad, cornerHeight: rad, transform: nil)); c.fillPath()
}

/// A: a Detroit coney, side elevation. Natural-casing dog in a soft bun, a band of beanless chili along the top, diced onions on the
/// chili and one mustard line. 6 colours with the background.
func coney(_ c: CGContext, _ s: CGFloat) {
    let BUN: UInt32 = 0xF0C98A, DOG: UInt32 = 0xB5452E, CHILI: UInt32 = 0x7A3A1C, ONION: UInt32 = 0xF7F1E3, MUSTARD: UInt32 = 0xF4C430
    rr(c, CGRect(x: 0.14 * s, y: 0.41 * s, width: 0.72 * s, height: 0.13 * s), 0.065 * s, DOG)                 // dog, ends showing
    rr(c, CGRect(x: 0.20 * s, y: 0.29 * s, width: 0.60 * s, height: 0.19 * s), 0.075 * s, BUN)                 // bun
    rr(c, CGRect(x: 0.23 * s, y: 0.50 * s, width: 0.54 * s, height: 0.12 * s), 0.06 * s, CHILI)                 // chili on top
    c.setStrokeColor(rgb(MUSTARD)); c.setLineWidth(0.0332 * s); c.setLineCap(.round); c.setLineJoin(.round)
    c.move(to: CGPoint(x: 0.28 * s, y: 0.535 * s))
    for i in 0..<4 { let x0 = 0.28 + Double(i) * 0.11
        c.addQuadCurve(to: CGPoint(x: (x0 + 0.11) * s, y: 0.535 * s), control: CGPoint(x: (x0 + 0.055) * s, y: (i % 2 == 0 ? 0.565 : 0.505) * s)) }
    c.strokePath()
    c.setFillColor(rgb(ONION))
    for (x, y) in [(0.27, 0.585), (0.37, 0.60), (0.47, 0.585), (0.57, 0.60), (0.67, 0.585)] {
        c.fill(CGRect(x: x * s, y: y * s, width: 0.043 * s, height: 0.043 * s))
    }
}

func render(_ n: Int, _ path: String) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(LAKE)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n))
    coney(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "MichiganEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png")
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name)
}

/// The share image (1200 x 630): deep lake, the coney at the left, the name and tagline at the right, the shoreline band (sand
/// beach line, lake-blue water) along the bottom.
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(LAKE)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    ctx.setFillColor(rgb(0xE3D5AE)); ctx.fill(CGRect(x: 0, y: 30, width: W, height: 12))
    ctx.setFillColor(rgb(0x1B6EA8)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: 30))
    ctx.saveGState(); ctx.translateBy(x: 20, y: 60); coney(ctx, 560); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 112) ?? NSFont.boldSystemFont(ofSize: 104)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 42) ?? NSFont.boldSystemFont(ofSize: 38)
    NSAttributedString(string: "MICHIGAN EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 560, y: 330))
    NSAttributedString(string: "CONEYS, PASTIES & SQUARE PIZZA", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 0.89, green: 0.84, blue: 0.68, alpha: 1)]).draw(at: NSPoint(x: 564, y: 272))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
