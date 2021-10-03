from googleapiclient import discovery
import json, ast

API_KEY = 'AIzaSyADbwqXX1O-Ppc9tfO6cC1_BaPeslXY-c4'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

analyze_request = {
  'comment': { 'text': 'hey i kinda like you' },
  'requestedAttributes': {"TOXICITY": {}, "INSULT": {}, "FLIRTATION": {}, "INCOHERENT": {}, "SPAM": {}}
}

response = client.comments().analyze(body=analyze_request).execute()

e = ast.literal_eval(json.dumps(response))

#e["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
