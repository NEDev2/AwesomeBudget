from flask import Flask, jsonify, request, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from tinydb import TinyDB
import pickle

app = Flask(__name__)
db = TinyDB('expenses.json')

train_titles = [
  # Original training data
  "Bought groceries",
  "Paid electricity bill",
  "Dinner at a restaurant",
  "Bought a new shirt",
  "Bought movie tickets",
  "Filled up fuel",
  "Bought a book",
  "Bought a gift",
  "Donated to charity",
  "Bought online course",
  "Bought video game",
  "Saved for vacation",
  "Invested in stocks",
  "Bought concert tickets",
  "Bought a laptop",
  "Bought a gadget",
  "Donated to local shelter",
  "Bought a new phone",
  "Bought a streaming app subscription",
  "Bought whey protein",
  "Bought a book on self-improvement",
  "Bought a chess book",
  "Bought my brother a new shirt",

  # More training data
  "Hospital bill after accident",
  "Car repairs after breakdown",
  "Unexpected house repairs",
  "Urgent travel expenses",
  "Emergency dental work",
  "Paid unexpected legal fees",
  "Last-minute flight ticket",
  "Medical bills for surgery",
  "Boiler replacement costs",
  "Emergency vet fees",
  "Replacing stolen items",
  "Urgent home plumbing fix",
  "Sudden loss of income savings",
  "Medication not covered by insurance",
  "Paying off unexpected debt",
  "Emergency locksmith services",
  "Quick funds for family emergency",
  "Roof repair after storm damage",
  "Bought stocks in tech company",
  "Invested in startup company",
  "Purchased bonds",
  "Real estate investment",
  "Started a retirement fund",
  "Bought shares in mutual funds",
  "Gold investment purchase",
  "Long-term fixed deposit",
  "Opened a new Roth IRA",
  "Cryptocurrency long-term hold",
  "Real estate property downpayment",
  "Long-term government bonds",
  "Invested in peer-to-peer lending",
  "Started a 401k account",
  "Saving for new laptop",
  "Saved for upcoming summer vacation",
  "Christmas holiday fund",
  "Setting aside money for new phone",
  "Saving up for concert tickets",
  "Funds for a weekend getaway",
  "Birthday party budget",
  "Saving up for a new bicycle",
  "Money aside for shopping spree",
  "Short-term savings for a camera",
  "New year's eve party budget",
  "Setting aside for festive shopping",
  "Enrolled in online course",
  "Bought new educational books",
  "Attended a professional workshop",
  "New musical instrument for classes",
  "Joined a new gym membership",
  "Subscribed to a language learning platform",
  "Bought art supplies for class",
  "Enrolled in culinary classes",
  "Attended a business seminar",
  "Subscribed to an educational magazine",
  "Annual library membership fee",
  "Paid tuition fees for online degree",
  "New pair of shoes",
  "Dinner at a luxury restaurant",
  "Went to see a movie",
  "Bought video games",
  "Shopping at the mall",
  "Weekend trip to the beach",
  "Purchased new clothing",
  "New smartphone purchase",
  "Bought gifts for family",
  "Grocery shopping",
  "Attended a music concert",
  "New gadgets for the kitchen",
  "Bought a new book",
  "Ordered takeaway food",
  "Bought accessories",
  "Gym membership renewal",
  "Purchased new furniture",
  "Bought cosmetics",
  "Tickets for a theatre show",
  "Donated to local orphanage",
  "Supported a friend's fundraiser",
  "Gave money to a homeless person",
  "Charity marathon participation fee",
  "Donated to flood relief",
  "Supported global health charities",
  "Donated to local school",
  "Charity concert ticket",
  "Supported community arts program",
  "Annual donation to favorite charity",
  "Contributed to community development"
]

train_labels = [
  # Original labels
  "Groceries",
  "Utilities",
  "Dining",
  "Shopping",
  "Entertainment",
  "Transportation",
  "Entertainment",
  "Gifts",
  "Generosity/Charity",
  "Education",
  "Entertainment",
  "Short-Term Savings/Goals",
  "Long-Term Investments",
  "Entertainment",
  "Shopping",
  "Shopping",
  "Generosity/Charity",
  "Shopping",
  "Entertainment",
  "Self-improvement/Education",
  "Self-improvement/Education",
  "Self-improvement/Education",
  "Generosity/Charity",

  # More labels
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Emergency Savings",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Long-Term Investments",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Short-Term Savings/Goals",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Self-improvement/ Education",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Personal Spending",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
  "Generosity/Charity",
]

train_labels.extend(["Generosity/Charity", "Generosity/Charity"])

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_titles)
classifier = MultinomialNB()
classifier.fit(X_train, train_labels)


@app.route('/spend_money', methods=['POST'])
def spend_money():
  data = request.json
  amount_spent = float(data.get('amount', 0))
  title = data.get('title', '')

  # Predict category using the ML model
  X_test = vectorizer.transform([title])
  predicted_category = classifier.predict(X_test)[0]

  db.insert({
    "amount": amount_spent,
    "title": title,
    "category": predicted_category
  })

  # Retrain the model with the new data
  global train_titles, train_labels
  train_titles.append(title)
  train_labels.append(predicted_category)
  X_train = vectorizer.fit_transform(train_titles)
  classifier.fit(X_train, train_labels)

  return jsonify({
    "message": "Expense added successfully",
    "category": predicted_category
  })


@app.route('/current_money', methods=['GET'])
def current_money():
  expenses = db.all()
  total_spent = sum([expense['amount'] for expense in expenses])
  current_money = 1000 - total_spent  # Assuming you started with 1000
  return jsonify({"current_money": current_money})


@app.route('/money_spent_this_month', methods=['GET'])
def money_spent_this_month():
  expenses = db.all()
  total_spent = sum([expense['amount'] for expense in expenses])
  return jsonify({"money_spent_this_month": total_spent})


@app.route('/expenses', methods=['GET'])
def expenses():
  return jsonify(db.all())


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False)
