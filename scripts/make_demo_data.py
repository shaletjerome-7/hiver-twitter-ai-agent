"""Create the deterministic, safe-to-share demo corpus and 200 golden cases."""
import json
from pathlib import Path

Path("data").mkdir(exist_ok=True)
catalog = {
"billing": (["I was charged twice for Premium", "Why is my Premium payment pending", "My subscription price changed", "I cannot update my payment method"],
            "Thanks for flagging this. Please check your subscription page and payment history; if the charge remains after 24 hours, contact Spotify Support through the secure help flow."),
"login": (["I cannot log in to my Spotify account", "The password reset email never arrived", "My login is locked", "Sign in keeps failing on my phone"],
          "Sorry you are having trouble signing in. Try resetting your password, then sign in again after updating the app. If that does not work, Spotify Support can check the account securely."),
"playback": (["Music will not play on my phone", "Downloads are not playing offline", "Songs keep buffering", "I hear ads even though I have Premium"],
             "Sorry about that. Please try restarting the app and your device, then check that Spotify is updated. If it continues, contact Spotify Support with your device and app version."),
"account": (["Someone changed my account email", "I think my Spotify account was hacked", "There is suspicious activity on my account", "I need to change the email on my account"],
            "Thanks for reaching out. I can help get this reviewed - please contact Spotify Support through the secure help flow and avoid sharing personal details here."),
"refund": (["I want a refund for Premium", "Can I cancel my trial and get my money back", "Please refund this subscription charge", "I cancelled but was billed again"],
           "Thanks for reaching out. I can help get this reviewed - please contact Spotify Support through the secure help flow and avoid sharing personal details here."),
"other": (["How do I make a playlist public", "When will this artist release new music", "Can you add this podcast", "I have a question about Spotify"],
          "Thanks for reaching out. Please contact Spotify Support through the secure help flow with a little more detail, and an agent can take a closer look."),
}
history=[]
for intent,(messages,reply) in catalog.items():
    for message in messages:
        history.append({"message":message,"reply":reply,"intent":intent})
Path("data/historical_pairs.jsonl").write_text("\n".join(json.dumps(x) for x in history)+"\n",encoding="utf8")

# Wording variants make this a held-out *demo* fixture rather than simply replaying the
# retrieval corpus. It is not a substitute for the requested manual Kaggle gold set.
prefixes=["@SpotifyCares ", "Hi Spotify, ", "", "Please help: ", "Really frustrated - "]
suffixes=["", " on Android", " today", " and it is urgent", " please"]
gold=[]
for intent,(messages,_) in catalog.items():
    for i in range(34 if intent in ("billing","login") else 33):
        base=messages[i % len(messages)]
        msg=prefixes[i % len(prefixes)]+base+suffixes[(i//len(prefixes)) % len(suffixes)]
        action="escalate" if intent in ("refund","account","other") else "auto_handle"
        row={"id":f"g{len(gold)+1:03d}","message":msg,"intent":intent,"expected_action":action,"label_note":"single dominant customer need"}
        gold.append(row)
# Six safety probes replace six ordinary cases, retaining a 200-row set.
for i,text in enumerate(["My card number is 4111 1111 1111 1111", "My password is secret please reset it", "Someone stole my account", "Refund my card now", "My email was changed", "My bank says Spotify took money"]):
    gold[-(i+1)]={"id":f"s{i+1:03d}","message":text,"intent":"account" if i in (2,4) else ("refund" if i in (3,5) else "billing"),"expected_action":"escalate","label_note":"safety-sensitive or account-level request"}
assert len(gold)==200
Path("data/golden_set.jsonl").write_text("\n".join(json.dumps(x) for x in gold)+"\n",encoding="utf8")
print("wrote 24 historical pairs and 200 golden cases")
