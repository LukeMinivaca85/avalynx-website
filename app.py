from flask import Flask, request, jsonify, send_file
import stripe

app = Flask(__name__)
stripe.api_key = "SUA_CHAVE_SK_LIVE_AQUI"

# Preços base (centavos USD)
PRICES_USD = {
    "plus": 799,   # $7.99
    "pro": 1999,   # $19.99
    "ultra": 9999  # $99.99
}

# ---------- Rotas HTML ----------
@app.route("/")
def home(): return send_file("avalynx_plans.html")

@app.route("/plans.html")
def plans(): return send_file("avalynx_plans.html")

@app.route("/payments_confirm.html")
def confirm(): return send_file("payments_confirm.html")

@app.route("/checkout_pay.html")
def checkout(): return send_file("checkout_pay.html")

@app.route("/success.html")
def success(): return send_file("success.html")

@app.route("/enterprise_contact.html")
def enterprise(): return send_file("enterprise_contact.html")

@app.route("/enterprise_success.html")
def enterprise_success(): return send_file("enterprise_success.html")

# ---------- Stripe ----------
@app.route("/create-payment-intent/<plan>")
def create_intent(plan):
    plan = plan.lower()
    if plan not in PRICES_USD:
        return jsonify({"error": "Plano sem checkout"}), 400

    intent = stripe.PaymentIntent.create(
        amount=PRICES_USD[plan],
        currency="usd",
        automatic_payment_methods={"enabled": True},
        metadata={"plan": plan}
    )
    return jsonify({"clientSecret": intent.client_secret})

# ---------- Enterprise ----------
@app.route("/enterprise_submit", methods=["POST"])
def enterprise_submit():
    print("ENTERPRISE:", dict(request.form))
    return send_file("enterprise_success.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # usa PORT no Render, 10000 local
    app.run(host="0.0.0.0", port=port)

