# Gulaverse ad placement: handoff

The client's ad (`gulaverse_creative.jpg`, 5:3) is placed onto real Kerala street footage, on billboards, an auto-rickshaw back and LED screens. Each clip is 3–4 s, vertical 9:16.

## Status (24 Oct 2026)
- **The client rejected round 1 as "weak".**
- My frame-by-frame tracked version (clip 1) **shakes**. Don't use that method again.
- **Next step: regenerate every clip in Seedance** with the edited first frames in `first_frames/`.

## Per-clip inputs

| Clip | Source video | Use from | First frame | Placement | Must stay in front |
|---|---|---|---|---|---|
| 1 | IMG_4483 | 0 s | clip1_FINAL_first_frame.jpg | Rooftop billboard (near-square board, navy padded at top) | — |
| 2 | IMG_4485 | **5 s → 9 s** (`trimmed_videos/clip2_trim_5s.mp4`) | clip2_FINAL_first_frame.jpg | LED screen at the junction | Yellow pole, "OXY WUD" sign |
| 3 | IMG_4486 | 0 s | clip3_FINAL_first_frame.jpg | Board over tiled roof (near-square, creative stretched) | Roof tiles at bottom-right |
| 4 | IMG_4490 | **2 s → end** (`trimmed_videos/clip4_trim_2s.mp4`) | clip4_FINAL_first_frame.jpg | Catalyst board (2.2:1, sides extended) | Street-light pole, electric post, crossarm, wires |
| 5 | IMG_9796 | 0 s | clip5_FINAL_first_frame.jpg | CP Plus board (2:1, sides extended), through a rainy windscreen | Power line, palm fronds |
| 6 | IMG_9799 | **1 s → 5 s** (`trimmed_videos/clip6_rickshaw_trim_1080p.mp4`) | clip6_FINAL_first_frame.jpg | Auto-rickshaw rear hood, through a rainy windscreen | Rain drops on the glass |
| 7 | IMG_9800 | 0 s | clip7_FINAL_first_frame.jpg | White billboard, dark rainy sky | Power line, tree branch, festive lights |
| 8 | IMG_9809 | 0 s (the first ~1 s is out of focus, so trim it after generating) | clip8_FINAL_first_frame.jpg | LED screen (whole shot out of focus) | Bamboo stick |
| 9 | IMG_9804 | 0 s | clip9_FINAL_first_frame.jpg | Big rooftop teaser board | — |

The original clips are on the user's device (Kerala footage, IMG_xxxx.MOV).

## Seedance workflow (per clip)
1. Upload the **source video** (trimmed if the table says so). Seedance uses it for the camera motion and the scene.
2. Upload the clip's **first frame** as **@Image1** and the **Gulaverse creative** as **@Image2**.
3. Set **9:16**, **1080p**, the same duration as the source (3–5 s).
4. Use the prompt below, filling in the [brackets].
5. Check the result: zoom in on നിങ്ങളുടെ, ഇനി, "MEDIA & MARKETING", 7356235566 and the GV logo. **Any broken text means regenerate.** Don't accept it.
6. If there is a watermark, remove it by cropping about 12% from the bottom-right (crop 950×1688 at x=65, then scale to 1080×1920).

### Prompt template (@ is used for images only)
```
Use the uploaded video as the base: keep its camera movement, handheld shake, traffic, people, buildings, sky, lighting and colours exactly the same.

The only change: the [BOARD DESCRIPTION] shows the Gulaverse ad exactly as in @Image1, for the whole clip, from the first frame to the last. Use @Image2 as the exact reference for the artwork: every letter of the Malayalam text (നിങ്ങളുടെ, ഇനി, നാലാളറിയും), "Brand", the GV logo, "Gulaverse MEDIA & MARKETING", the phone number 7356235566 and the address must stay identical and sharp. Do not redraw or invent any text or logo.

The ad is a real [printed flex billboard / LED screen / vinyl banner on the rickshaw hood]: it stays rigidly locked to the [board / screen / hood] with no sliding, wobble or warping, follows the camera motion and perspective, and matches the scene's [overcast daylight / rainy windscreen haze / out-of-focus blur]. [OCCLUDERS] stay in front of it. Change nothing else.
```

## Lessons from round 1
- Nano Banana got the phone number wrong once (7366…). Always check the number.
- The AI video tools garble the small Malayalam text and "MEDIA & MARKETING". This was the client's main complaint.
- Realism needs **things in front** of the ad (wires, poles, palms, rain) and the board's own texture (seams, light falloff). That's how the first frames were built.
- Board shapes don't match the 5:3 creative on clips 1 and 3 (square) or clips 4 and 5 (wide). **Ask the designer for 1:1 and 2:1 versions** for best accuracy.
- The frame-by-frame overlay (`tools/fix_text.py`, `tools/track_place.py`) caused visible shake. Avoid it, or smooth the tracking much more heavily.
