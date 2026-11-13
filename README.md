# Trust and Hope

*Learn how to support someone you love — and how to let someone support you.*

A browser game about mental health, made by **W4GZ (Writing for Gen Z)**.

▶️ **Play:** [anbu47.github.io/W4GZ-mental-health-supporter](https://anbu47.github.io/W4GZ-mental-health-supporter/)

## Two parts, one story

After choosing your characters, pick a part:

| | Part 1 · Trust Recovery | Part 2 · Hope Recovery |
|---|---|---|
| **You are** | the supporter | the one who is struggling |
| **Your loved one** | is going through a hard time | is there to help you |
| **The bar** | Trust | Hope |
| **Answers** | ✅ Supportive · 🙂 Well-meant · ❌ Hurtful | ✅ Letting them in · 🙂 Half-open · ❌ Shutting them out |

## How to play

1. **Choose your characters.** Pick yourself and your loved one (man, woman or non-binary). Names are optional.
2. **Explore the house.** Six rooms open chapter by chapter (Week 1 → Week 3 → Month 2): Living Room, Kitchen, Study, Balcony, Your Corner and Bedroom. Each room has two faded objects; tap one to start a moment with your loved one.
3. **Read and respond.** The situation types out, your loved one speaks, and you choose an answer. Every answer has a spoken line, and your loved one replies to what you said.
   - ✅ Supportive: the object lights up fully, **+4**.
   - 🙂 Well-meant: the object is only half-lit, **+2**. Come back later and choose the supportive answer for another **+2**.
   - ❌ Hurtful: the object stays dark, **−10**.
   - 🔥 Supportive answers in a row earn a streak bonus (+1, +2, then +3).
4. **Heart moments.** Five 💗 hearts sit on the bar. Reaching each one unlocks a heart conversation with **1 chance only**: a supportive answer wins the heart (+5); otherwise it's lost (a hurtful answer costs −20).
5. **Energy.** Every talk costs 🔋 energy. Recharge when it runs low: some ways to rest work better than others (in Part 2 these are *self-love actions*).
6. **Bad days.** As the weeks pass, a light may go out. Answer well to relight it — recovery isn't a straight line.
7. **The Bedroom.** The last room opens when every other object is lit and trust reaches 60. It holds the hardest night.
8. **Trust or hope at 0.** The first time it hits 0, you get a warning. One more hurtful answer while it's at 0 and the story ends, taking you back to choose a part.

## Questions

There are **120 real-life questions**: 60 in each part, 10 in every room (a pool of 5 for each object). Every new game draws a fresh random set of 12, so no two playthroughs are the same. In the Bedroom, the first object always draws a crisis opener and the second a safety follow-up.

The full bank — situations, answers, spoken lines, replies and explanations — is in [`questions.json`](questions.json).

## The ending

- **Mental rank:** your rank comes from the hearts you won — 🪨 Iron, 🥉 Bronze, 🥈 Silver, 🥇 Gold, 💎 Diamond or 👑 Legend.
- **🔍 Look back:** a list of every moment where you didn't pick the best answer. Tap one to see what you chose, the reply it got, and a more supportive answer with why it works. Moments you fixed later are marked ✓ Fixed.
- **🏁 See my result:** if every room is lit but some objects are only half-lit, you can finish early.

## Sound

Everything is made in code with the Web Audio API — no audio files.

- 🎵 **Music:** a calm piano-and-pad soundtrack that follows the mood, warmer as trust or hope grows. Tap 🎵 to turn it on or off.
- 🗣️ **Game voice:** characters "speak" in soft blips as their words type out, with a different pitch for each character.

## Help and safety

This game is for learning. It is not a substitute for professional help.

Tap **♡ Help** at any time — on the front page or in the game — for crisis support. If someone may be in danger, contact your local emergency number. To find a free, confidential helpline in your country, visit [findahelpline.com](https://findahelpline.com).

## Files

| File | What it is |
|---|---|
| `index.html` | The whole game in one file. Open it in any browser, phone or desktop. |
| `questions.json` | The question bank (also built into `index.html`). |
