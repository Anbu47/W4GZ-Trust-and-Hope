# Trust and Hope

*Learn how to support someone you love — and how to let someone support you.*

A browser game about mental health, made by **W4GZ (Writing for Gen Z)**.

▶️ **Play:** [anbu47.github.io/W4GZ-Trust-and-Hope](https://anbu47.github.io/W4GZ-Trust-and-Hope/)

## Language · Ngôn ngữ

The game opens in **Tiếng Việt** by default. Tap **🌐 Ngôn ngữ / Language** on the front page to switch between Tiếng Việt and English. The choice is remembered on this device, and you can also link to a language directly with `?lang=vi` or `?lang=en`.

The Vietnamese text lives in [`lang/vi.js`](lang/vi.js), keyed by the original English text, so the English stays exactly as it is. The Vietnam hotline matching below is shown only in Vietnamese.

## Hotline matching · Vietnam

Choose **Ghép cặp đường dây nóng** to match five Vietnam hotlines with the needs they support. Correct matches open the full contact card, with clickable telephone numbers, opening hours, audience information and official links. Matched hotline cards can be opened again. Retry without penalties, replay, or return to part selection to start Part 1 or Part 2.

The former Part 0 house and quiz have been removed. Parts 1 and 2 continue to use `questions.json` and include **Go back** (return to the house) and **Back to home** (return to the title screen) on questions.

The matching activity and Help panel include Ngày Mai, HOPE, the National Child Helpline, CSAGA and Peace House. Every push to `main` runs the [automatic Find A Helpline check](docs/hotline-checks.md). Verification dates are only shown for successfully checked, matching contact content. HOPE’s hours are not published in its directory profile and are not automatically verified there.

## Two story parts

After choosing your characters, pick a part:

| | Part 1 · Trust Recovery | Part 2 · Hope Recovery |
|---|---|---|
| **You are** | the supporter | the one who is struggling |
| **Your loved one** | is going through a hard time | is there to help you |
| **Lives** | ❤️❤️❤️ | ❤️❤️❤️ |
| **Answers** | ✅ Supportive · 🙂 Well-meant · ❌ Hurtful | ✅ Letting them in · 🙂 Half-open · ❌ Shutting them out |

## How to play

1. **Choose your characters.** Pick yourself and your loved one (man, woman or non-binary). Names are optional.
2. **Explore the house.** Six rooms open chapter by chapter (Week 1 → Week 3 → Month 2): Living Room, Kitchen, Study, Balcony, Your Corner and Bedroom. Each room has two faded objects; tap one to start a moment with your loved one.
3. **Read and respond.** The situation types out, your loved one speaks, and you choose an answer. Every answer has a spoken line, and your loved one replies to what you said.
   - ❌ Hurtful answers **blink light red** as soon as the question appears, so players learn to spot what hurts.
   - ✅ Supportive and 🙂 Well-meant answers count the same: the object lights up fully. The explanation still shows how each one helps.
   - ❌ Hurtful: the object stays dark and you lose **1 ❤️**. Come back later and choose a better answer.
   - There is no score: the top bar only shows your **❤️ lives** and **✨ x/12** lit objects.
4. **Heart moments.** A 💗 heart conversation appears after 2, 4, 6, 8 and 11 lit objects, with **1 chance only**. A warning shows before you answer. Any non-hurtful answer wins the heart and **gives back 1 ❤️** (up to 3); a hurtful answer loses the heart and costs **2 ❤️**.
5. **Energy.** Every talk costs 🔋 energy. Recharge when it runs low: some ways to rest work better than others (in Part 2 these are *self-love actions*).
6. **Bad days.** As the weeks pass, a light may go out. Answer well to relight it — recovery isn't a straight line.
7. **The Bedroom.** The last room opens when every other object is lit. It holds the hardest night.
8. **Lives.** You start with 3 ❤️. When you drop to 1 ❤️ you get a warning. Lose all 3 and the house goes dark: the story ends and you choose a part to start again.

## Questions

There are **120 real-life questions**: 60 in each part, 10 in every room (a pool of 5 for each object). Every new game draws a fresh random set of 12, so no two playthroughs are the same. In the Bedroom, the first object always draws a crisis opener and the second a safety follow-up.

The full bank — situations, answers, spoken lines, replies and explanations — is in [`questions.json`](questions.json).

## The ending

- **Mental rank:** your rank comes from the hearts you won — 🪨 Iron, 🥉 Bronze, 🥈 Silver, 🥇 Gold, 💎 Diamond or 👑 Legend.
- **🔍 Look back:** a list of every moment where you didn't pick the best answer. Tap one to see what you chose, the reply it got, and a more supportive answer with why it works. Moments you fixed later are marked ✓ Fixed.
- **🏁 See my result:** if every room is lit but some objects are only half-lit, you can finish early.

## Colour themes

Two themes built from the W4GZ brand guideline (v3.2). Tap 🌙 / ☀️ on the front page to switch; your choice is remembered.

- ☀️ **Light sky** (default): pale blue page, navy text, white cards.
- 🌙 **Soft dusk**: mid-navy page, paper-white text, pale sky-blue buttons.

## Sound

Voices and sound effects are made in code with the Web Audio API; the music is one small MP3 file.

- 🎵 **Music:** an original trap-style loop — trap drums and 808 bass, lead guitar (with a guitar solo), hummed "mmm / ooh / aah" vocals and a few "ting ting" bells — in [`music/trap-loop.mp3`](music/trap-loop.mp3). It loops seamlessly (about 2 minutes). If the file can't load (for example, when `index.html` is opened on its own), a calm piano soundtrack made in code plays instead. Tap 🎵 to turn it on or off.
- 🗣️ **Game voice:** characters "speak" in soft blips as their words type out, with a different pitch for each character.

## Help and safety

This game is for learning. It is not a substitute for professional help.

Tap **♡ Help** at any time — on the front page or in the game — for crisis support. If someone may be in danger, contact your local emergency number. To find a free, confidential helpline in your country, visit [findahelpline.com](https://findahelpline.com).

## Files

| File | What it is |
|---|---|
| `index.html` | The whole game in one file. Open it in any browser, phone or desktop. |
| `questions.json` | The question bank (also built into `index.html`). |
| `lang/vi.js` | Vietnamese translations of every on-screen string, keyed by the English original. |
