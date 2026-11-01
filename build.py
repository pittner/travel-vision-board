#!/usr/bin/env python3
"""Builds index.html for pittner/travel-vision-board.

A single-purpose page for the "travel vision board" / "travel goals 2027" search intent (trips are
planned in December and January): 36 travel goals in 6 groups (dream trips, budget, adventures, close
to home, travel with people you love, travel better), each with why it matters and a first step;
one click opens the free maker prefilled as a phone lock screen. Plus 12 questions, a 45-minute plan,
a box for your own goal, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/travel-vision-board/"
SRC = "ghpages_travel"
CAMPAIGN = "travel_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Dream trips", [
        ("Visit Japan in spring 2027", "A trip you name and date is a trip you plan; a someday trip stays someday.", "Pick the month and look up one round-trip flight price today"),
        ("See the Northern Lights", "Some places are only magic at one time of year, so it has to be planned.", "Choose a country and the best month, and write it on your board"),
        ("Take one trip I have postponed for years", "The trip you keep postponing is usually the one you want most.", "Write down why you postponed it and the one thing that would unblock it"),
        ("Travel to a new continent", "A different continent changes how you see your own daily life.", "List three places you would go and circle the cheapest to reach"),
        ("Do a road trip with no fixed plan", "Freedom on the road is a feeling you cannot buy in a package tour.", "Pick the start city and the first night's stay"),
        ("See one wonder of the world", "Standing in front of something you saw in school photos stays with you forever.", "Choose one and check the season with the fewest crowds"),
    ]),
    ("Budget and saving", [
        ("Save for travel every month", "A dedicated travel fund turns dreaming into booking.", "Open a separate travel savings pot and set an automatic monthly amount"),
        ("Know the real cost of my dream trip", "A number makes the trip feel possible instead of vague.", "Add flights, stays, food and extras for your trip in one note"),
        ("Book flights at the right time", "Booking smart can save as much as a whole extra night away.", "Set a price alert for your main route today"),
        ("Travel on points and miles", "Rewards you already earn can pay for a flight if you collect them on purpose.", "Check the balance of every loyalty programme you have"),
        ("Take one trip for under 300 EUR", "Cheap trips prove you do not need a big budget to travel.", "Find the cheapest weekend flight from your city in the next three months"),
        ("Travel without card debt", "A trip paid in advance feels lighter than one you pay off for months.", "Divide the trip cost by the months left and save that each payday"),
    ]),
    ("Adventures", [
        ("Hike a famous trail", "Days on foot make a place yours in a way a bus tour never does.", "Pick the trail and train with one longer walk this weekend"),
        ("Learn to dive or snorkel", "Half the planet is under water and most people never see it.", "Find the nearest pool course or a beginner dive centre at your destination"),
        ("Sleep under the stars", "One night outside resets how you think about comfort.", "Find a dark-sky spot within three hours of home"),
        ("Do one thing that scares me a little", "Small fear on a trip turns into a big story at home.", "Write the one thing and the trip where you will do it"),
        ("Go somewhere where I do not speak the language", "Getting by with gestures and a smile builds real confidence.", "Learn ten words in that language this week"),
        ("Take a train across a country", "Slow travel shows the land between the famous cities.", "Look up one long scenic train route and its price"),
    ]),
    ("Close to home", [
        ("Explore my own country more", "Most people know foreign cities better than the next region.", "Pick three places within a day's drive you have never seen"),
        ("Take one weekend trip every season", "Four short trips a year beat one big trip you never take.", "Put four weekends in your calendar now, one per season"),
        ("Be a tourist in my own city", "Seeing home with fresh eyes costs nothing and feels like a holiday.", "Book one museum or guided walk you have never done"),
        ("Visit a friend who lives far away", "Friendships fade without visits; a trip keeps them alive.", "Message them today and suggest two possible dates"),
        ("Go camping at least twice", "Cheap, close nature trips recharge more than another weekend on the sofa.", "Borrow or check the gear you need for one night"),
        ("Do a day trip by train once a month", "Small regular escapes keep the travel feeling alive between big trips.", "Choose the first destination and check the timetable"),
    ]),
    ("Travel with people I love", [
        ("Take a trip with my partner, just us", "Time away without daily chores is when couples really talk.", "Agree on dates and a budget this week"),
        ("Travel with my kids somewhere new", "Kids remember trips long after they forget toys.", "Ask each child where they would love to go and write it down"),
        ("Take my parents on a trip", "Trips with parents become the memories you are most grateful for later.", "Ask them about one place they always wanted to see"),
        ("Plan a trip with my best friends", "Group trips happen only when one person picks a date.", "Send the group two date options and one destination idea"),
        ("Go on one solo trip", "Travelling alone shows you what you really enjoy.", "Pick a safe, easy city for a first solo weekend"),
        ("Meet locals, not just sights", "Conversations with people are what you tell stories about.", "Look up one local food tour, class or meetup at your destination"),
    ]),
    ("Travel better", [
        ("Pack carry-on only", "Light luggage means cheaper flights and freer days.", "Make a packing list that fits in one cabin bag"),
        ("Keep a travel journal or photo book", "Memories fade fast unless you keep them somewhere.", "Buy a small notebook or create one album for your next trip"),
        ("Travel slower: fewer places, more days", "Rushing from place to place leaves you tired, not full.", "Cut one stop from your next itinerary"),
        ("Take a real offline holiday", "A week without work email is when rest actually starts.", "Set the out-of-office dates and tell your team now"),
        ("Travel more sustainably", "Trains, longer stays and local food are kinder to places you love.", "Check if one trip this year can be done by train instead of a flight"),
        ("Renew my passport before I need it", "An expired passport has cancelled more dream trips than money.", "Check the expiry date of your passport today"),
    ]),
]

QUESTIONS = [
    "Which trip in 2026 do I still think about, and why?",
    "Where did I want to go this year but did not, and what stopped me?",
    "Do I want rest, adventure or connection from travel in 2027?",
    "Who do I want to travel with next year?",
    "How much did I spend on travel in 2026, roughly?",
    "What would make a trip feel worth every euro to me?",
    "Which place have I wanted to see since I was a child?",
    "How many days off do I really have in 2027?",
    "What small trip could I take in the next three months?",
    "What do I always overpack or overplan?",
    "Which travel fear could I face next year?",
    "If 2027 goes really well, which trip photo is on my phone by next December?",
]

PLAN = [
    ("10 minutes: look back honestly.", "Scroll through your 2026 photos and note which trips gave you energy and which only cost money."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three trips.", "Not ten. One big trip, one weekend escape, one trip with someone you love."),
    ("10 minutes: make it visible.", "Turn your dream trip and its first step into a phone lock screen, so you see it every day until you book it."),
]

FAQ = [
    ("What should go on a travel vision board?",
     "Put the place in your own words with a month, a first step you can do this week, and your reason why. "
     "This page has 36 travel goals in 6 groups (dream trips, budget, adventures, close to home, travelling with people you love, travelling better), each with a first step, so you can pick three and make them visible."),
    ("Does a travel vision board actually work?",
     "A board does not book flights by itself, but seeing the trip every day keeps it in front of you when you decide what to spend on. "
     "The habit that works best is putting it on your phone lock screen."),
    ("How many trips should I plan for 2027?",
     "Three is enough: one big trip, one weekend escape and one trip with someone you love. Fewer plans get booked more often."),
    ("How do I afford my dream trip in 2027?",
     "Know the real cost, divide it by the months left and save that amount automatically every payday. Add price alerts and points you already collect."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full travel vision board with all my trips?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Travel Vision Board 2027: %%COUNT%% Travel Goals with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% travel goals for 2027 (dream trips, budget, adventures, weekends close to home, trips with loved ones, travelling better), each with a first step for this week, %%NQ%% questions and a 45-minute plan. Free lock screen maker.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Travel vision board 2027 - %%COUNT%% travel goals with a first step and a free lock screen">
<meta property="og:description" content="Dream trips, weekend escapes and travel budget goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Travel vision board 2027: %%COUNT%% travel goals with a first step for this week</h1>
  <p class="lede">Most travel dreams stay dreams because there is no date, no budget and no first step. Below are %%COUNT%% travel goals for 2027, from dream trips to cheap weekend escapes, each with why it matters and a first step you can do this week, plus %%NQ%% questions to find out what kind of travel you really want. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see your next trip every day until you book it.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My travel goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. See Japan in cherry blossom season" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Set a flight price alert today" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions before you choose your trips</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your travel year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full travel vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/travel-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
