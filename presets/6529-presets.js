// 6529 Memes Glitch Art Presets for GIF//ME
// Format compatible with GIF//ME's PRESETS object
// https://gif-me.netlify.app/
//
// To use: merge these into the PRESETS object in gifme_script.js
// or load via browser console: Object.assign(PRESETS, PRESETS_6529)
//
// Style categories:
//   *-preserve = palette-preserving, subtle motion only
//   *-static = no-motion, glitch texture only (image stays fixed)
//   others = with motion + glitch effects

const PRESETS_6529 = {
  // Card #1 - 6529Seizing: subtle grain + gentle drift, palette preserved
  '6529-preserve': {noise:6, ntype:'grain', scan:3, sgap:2, mzoom:5, mdrift:3, msway:2, echo:3, glow:3, vig:4, sat:102, con:104},

  // Card #1 - Silkscreen variant
  '6529-silkscreen': {con:140, half:85, hcell:6, hang:45, duo:1, duoS:'#12081f', duoH:'#ff4fd8', duoMix:100, noise:8, mzoom:5, mdrift:3},

  // Card #2 - SeizeJPGs: heavy grain, RGB split, boiling effect
  '6529-boil': {con:120, noise:60, nsize:3, rgb:2, mzoom:8, mdrift:5},

  // Card #3 - UncleSeize: posterize + scanlines + pulse motion
  '6529-poster-pulse': {post:4, noise:10, ntype:'grain', scan:15, rgb:3, mzoom:6, msway:4, echo:5, sat:110, con:120},

  // Card #4 - NakamotoFreedom: warm amber glow, gentle drift
  '6529-amber-glow': {glow:20, sat:115, bri:105, noise:5, ntype:'grain', mzoom:4, mdrift:2, msway:2, echo:3, vig:6},

  // Card #6 - DALL-E's Revenge: pixel sort + RGB + scanlines
  '6529-seize-humans': {psort:15, pdir:1, noise:12, ntype:'grain', rgb:4, scan:20, mzoom:6, mdrift:4, echo:8, con:115},

  // Card #7 - Aeroglyph6529 Night: CRT interference, scanlines, static noise
  '6529-night-interference': {scan:35, sgap:2, rgb:5, noise:8, ntype:'static', glow:15, vig:20, sat:105, mzoom:3, mdrift:2},

  // Card #7 - Aeroglyph6529 Day: lighter interference, brighter
  '6529-day-interference': {scan:30, sgap:2, rgb:4, noise:6, ntype:'static', glow:20, sat:110, bri:105, mzoom:3, mdrift:2},

  // Card #8 - FirstGM: keypress glitch, crush + shake + RGB
  '6529-keypress-glitch': {crush:8, noise:15, ntype:'line', rgb:6, scan:25, mshake:4, echo:6, con:120},

  // Card #9 - The Institutions Are Coming: vintage film, faded palette
  '6529-vintage-preserve': {ntype:'film', noise:12, vig:30, con:112, bri:104, sat:80, glow:8, mzoom:3, mdrift:2, msway:1, echo:2},

  // Card #10 - A Meditation on GM: ocean hue shift, gentle glow
  '6529-ocean-trance': {hue:10, sat:115, glow:15, noise:6, ntype:'grain', mzoom:5, mdrift:3, msway:3, echo:4, vig:8},

  // Card #12 - OMSeized: deep ocean, subtle scanlines
  '6529-ocean-depth': {hue:-5, sat:108, con:110, glow:10, noise:8, ntype:'grain', scan:5, mzoom:4, mdrift:2, msway:2, echo:3, vig:10},

  // Card #13 - BlueGM: serene blues, very subtle motion
  '6529-serenity-preserve': {noise:5, ntype:'grain', mzoom:4, mdrift:2, msway:2, echo:2, glow:3, vig:4, sat:101, con:102},

  // Card #14 - GMgm: connection pulse, gentle breathing
  '6529-connection-pulse': {noise:5, ntype:'grain', mzoom:3, mdrift:2, msway:2, echo:3, glow:4, vig:5, sat:101, con:102},

  // Card #15 - GM to DEATH: spirit walk, psychedelic hue cycling
  '6529-spirit-walk': {hue:5, sat:105, noise:6, ntype:'grain', scan:4, rgb:2, mzoom:3, mdrift:2, msway:2, echo:3, glow:5, vig:4},

  // Card #16 - OMbuidling: static B&W, film grain + faint scanlines, NO motion
  '6529-foundation-pulse': {noise:6, ntype:'film', scan:2, sgap:2, mzoom:0, mdrift:0, msway:0, mshake:0, echo:0, glow:3, vig:4, sat:100, con:104},

  // Card #17 - Awakening OM: data bloom, pixel sort + posterize, NO motion
  '6529-data-bloom': {psort:6, post:7, noise:7, ntype:'line', crush:4, mzoom:0, mdrift:0, msway:0, mshake:0, echo:0, scan:8, glow:3, vig:4, sat:105, con:104},

  // Card #18 - OM Breakdown of the Bicameral Mind: RGB split, NO motion
  '6529-bicameral-split': {rgb:4, noise:6, ntype:'grain', scan:10, sgap:2, mzoom:0, mdrift:0, msway:0, mshake:0, echo:0, glow:3, vig:5, sat:102, con:105},

  // Card #20 - Hardware Wallet and Mug: cold storage, pixel sort, NO motion
  '6529-cold-storage': {psort:5, post:6, crush:3, noise:8, ntype:'grain', scan:12, sgap:2, mzoom:0, mdrift:0, msway:0, mshake:0, echo:0, glow:3, vig:4, sat:103, con:106},

  // Card #24 - NFT Adoption Pathway 2030: boardroom, pixel sort, NO motion
  '6529-boardroom': {psort:6, post:6, crush:4, noise:7, ntype:'grain', scan:10, sgap:2, mzoom:0, mdrift:0, msway:0, mshake:0, echo:0, glow:3, vig:4, sat:104, con:105},

  // Card #25 - Authentic Summer: certificate glitch, scanlines + posterize
  '6529-certificate': {scan:20, sgap:2, rgb:3, noise:10, ntype:'grain', post:4, mzoom:4, mdrift:3, msway:2, echo:4, glow:5, vig:8, sat:108, con:115},

  // Card #534 - The King Must Fall: preserve, subtle motion
  '6529-king-preserve': {noise:5, ntype:'grain', mzoom:3, mdrift:2, msway:1, echo:2, glow:3, vig:4, sat:101, con:102},
};

// Total: 22 presets
// Usage: Object.assign(PRESETS, PRESETS_6529)
// Then buttons with data-preset="6529-preserve" etc. will work automatically