// Michigan Eats icon concepts, Eats Ranked style v1 (../state-prompts/ICON-STYLE.md): one flat, level, centred food on a plain
// background. Usage: swift scripts/icon-concepts.swift <outdir> -> mi-A-coney.png, mi-B-square.png, mi-C-pasty.png (1024)
// Background: a deep lake navy (Honolulu blue #0076B6 darkened), so light and mid foods clear 3:1. CoreGraphics y is up.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let NAVY: UInt32 = 0x0D3F63   // deep lake (Nick 2026-10-22 palette)

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
    c.setStrokeColor(rgb(MUSTARD)); c.setLineWidth(34); c.setLineCap(.round); c.setLineJoin(.round)
    c.move(to: CGPoint(x: 0.28 * s, y: 0.535 * s))
    for i in 0..<4 { let x0 = 0.28 + Double(i) * 0.11
        c.addQuadCurve(to: CGPoint(x: (x0 + 0.11) * s, y: 0.535 * s), control: CGPoint(x: (x0 + 0.055) * s, y: (i % 2 == 0 ? 0.565 : 0.505) * s)) }
    c.strokePath()
    c.setFillColor(rgb(ONION))
    for (x, y) in [(0.27, 0.585), (0.37, 0.60), (0.47, 0.585), (0.57, 0.60), (0.67, 0.585)] {
        c.fill(CGRect(x: x * s, y: y * s, width: 44, height: 44))
    }
}

/// B: a Detroit-style square pizza seen from above: a rectangle with the caramelized cheese edge (frico) as a frame, brick cheese
/// inside, two "racing stripes" of sauce ladled on top and cupped pepperoni. Crisp corners. 5 colours.
func square(_ c: CGContext, _ s: CGFloat) {
    let EDGE: UInt32 = 0xC9843A, CHEESE: UInt32 = 0xF4D27A, SAUCE: UInt32 = 0xC0392B, PEP: UInt32 = 0x8E2418
    let r = CGRect(x: 0.14 * s, y: 0.255 * s, width: 0.72 * s, height: 0.47 * s)
    c.setFillColor(rgb(EDGE)); c.fill(r)
    c.setFillColor(rgb(CHEESE)); c.fill(r.insetBy(dx: 0.055 * s, dy: 0.055 * s))
    c.setStrokeColor(rgb(SAUCE)); c.setLineWidth(0.07 * s); c.setLineCap(.round)
    for y in [0.42, 0.57] {                                                         // two ladled stripes, gently wavy
        c.move(to: CGPoint(x: 0.24 * s, y: y * s))
        c.addCurve(to: CGPoint(x: 0.76 * s, y: y * s), control1: CGPoint(x: 0.41 * s, y: (y + 0.04) * s), control2: CGPoint(x: 0.59 * s, y: (y - 0.04) * s))
        c.strokePath()
    }
    c.setFillColor(rgb(PEP))
    for (x, y) in [(0.28, 0.33), (0.50, 0.33), (0.72, 0.33), (0.39, 0.475), (0.61, 0.475), (0.28, 0.632), (0.72, 0.632)] {
        c.fillEllipse(in: CGRect(x: x * s - 34, y: y * s - 34, width: 68, height: 68))
    }
}

/// C: a Yooper pasty, front elevation: a half-moon lying on its flat side, a lighter top plane where the crust domes, the crimped
/// rope along the arc as a darker band with diagonal crimp marks, and three steam slits cut through to the background. 4 colours.
func pasty(_ c: CGContext, _ s: CGFloat) {
    let CRUST: UInt32 = 0xD9A05B, TOP: UInt32 = 0xE8BE82, CRIMP: UInt32 = 0xB97E3E
    let cx = 0.5 * s, base = 0.30 * s, rx = 0.36 * s, ry = 0.40 * s
    func dome(_ inset: CGFloat) -> CGPath {
        let p = CGMutablePath()
        p.move(to: CGPoint(x: cx - rx + inset, y: base))
        p.addCurve(to: CGPoint(x: cx, y: base + ry - inset), control1: CGPoint(x: cx - rx + inset, y: base + ry * 0.75), control2: CGPoint(x: cx - rx * 0.55, y: base + ry - inset))
        p.addCurve(to: CGPoint(x: cx + rx - inset, y: base), control1: CGPoint(x: cx + rx * 0.55, y: base + ry - inset), control2: CGPoint(x: cx + rx - inset, y: base + ry * 0.75))
        p.closeSubpath(); return p
    }
    c.setFillColor(rgb(CRIMP)); c.addPath(dome(0)); c.fillPath()                    // crimp band = the outer 60 px of the arc
    c.setFillColor(rgb(CRUST)); c.addPath(dome(0.06 * s)); c.fillPath()
    c.saveGState(); c.addPath(dome(0.06 * s)); c.clip()                             // lighter top plane
    c.setFillColor(rgb(TOP)); c.fill(CGRect(x: 0, y: base + 0.15 * s, width: s, height: s))
    c.restoreGState()
    c.setStrokeColor(rgb(TOP)); c.setLineWidth(34); c.setLineCap(.round)
    for t in [0.14, 0.29, 0.43, 0.57, 0.71, 0.86] {                                  // crimp folds, slanted along the rope
        let a = Double.pi * (1 - t)
        let x = cx + CGFloat(cos(a)) * (rx - 0.03 * s), y = base + CGFloat(sin(a)) * (ry - 0.03 * s)
        let tx = CGFloat(-sin(a) * Double(rx)), ty = CGFloat(cos(a) * Double(ry)), n = hypot(tx, ty)
        let ux = tx / n, uy = ty / n, k: CGFloat = 0.7071                             // tangent turned 45 degrees
        let dx = (ux * k - uy * k) * 13, dy = (ux * k + uy * k) * 13
        c.move(to: CGPoint(x: x - dx, y: y - dy)); c.addLine(to: CGPoint(x: x + dx, y: y + dy))
    }
    c.strokePath()
    c.setStrokeColor(rgb(NAVY)); c.setLineWidth(36)
    for dx in [-0.11, 0.0, 0.11] {                                                   // steam slits
        c.move(to: CGPoint(x: cx + dx * s, y: base + 0.17 * s)); c.addLine(to: CGPoint(x: cx + dx * s, y: base + 0.25 * s))
    }
    c.strokePath()
}

let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "."
func render(_ name: String, _ f: (CGContext, CGFloat) -> Void) {
    let ctx = CGContext(data: nil, width: 1024, height: 1024, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true); ctx.setFillColor(rgb(NAVY)); ctx.fill(CGRect(x: 0, y: 0, width: 1024, height: 1024))
    f(ctx, 1024)
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out + "/" + name) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil); CGImageDestinationFinalize(d)
}
render("mi-A-coney.png", coney); render("mi-B-square.png", square); render("mi-C-pasty.png", pasty)
print("ok")
