var rl = require('readline');

var path = "/vagrant/plugins/"

function AddWordsToCorpus(words,corpus,dict)
{
  for (var j=0; j < words.length; j++)
  {
    var ideas = dict[words[j].toLowerCase()];
    if (ideas != null)
    {
      for (var k=0; k < ideas.length; k++)
      {
        if (corpus[ideas[k][1]] == null)
        {
          corpus[ideas[k][1]] = []; 
        }
        corpus[ideas[k][1]].push(ideas[k][0]);
      }
    }
    
  }
  
}

function GenerateCorpus(twitter_id, tweet)
{
  
  var phrase = "lang:en+from:" + twitter_id; // English languate tweets sent to @labnol
  var search = "https://api.twitter.com/1.1/search/tweets.json?count=500&include_entities=false&q="; 
  search = search + encodeString(phrase);
  var tweets = GetRequest(search).statuses;
  
  
  
  var dict = LoadDictionary();
  //print"dict loaded");
  
  var thewords = {};
  var thesewords = {};
  
  for (var i=tweets.length; i>=0; i--) 
  {
    var words = "";
    if (i == tweets.length)
    {
      words =  tweet.replace(/[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]/g," ").split(' ');
      AddWordsToCorpus(words,thewords,dict);
      AddWordstoCorpus(words,thesewords,dict); 
    }
    else
    {
      words = tweets[i].replace(/[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]/g," ").split(' ');
      AddWordsToCorpus(words,thewords,dict);
    }
  }
  return [thewords,thesewords];
}


var fs = require('fs');

function LoadDictionary()
{
    return JSON.parse(fs.readFileSync(path + "ideas_json",'utf-8'));
}

function LoadCoOccuranceDict()
{
    return JSON.parse(fs.readFileSync(path + "CoOcc.txt",'utf-8'));
}


function encodeString (e)
{
    return e;  
}


//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
function shuffle(o){ //v1.0
  for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
  return o;
}

function chooseResponse(tweets, maxtrials, file)
{
  var dict = LoadDictionary();
  var coOccuranceDict = LoadCoOccuranceDict();
    
  for (var t = 0; t < maxtrials; t++)
  {
    
    var corpus = {};
    
//    console.log("Original Tweet = " + tweets[0]);
    AddWordsToCorpus(tweets[0].replace(/[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]/g," ").split(' '),corpus,dict);
    AddWordsToCorpus(tweets[0].replace(/[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]/g," ").split(' '),corpus,dict);

     
    var tweet_ix = 1;
 
      
    var sentence = getRandomSentence(file).split(' ');
      
    var response = "";
    var used_words = [];
    var last_word_a = false;
   
    for (var i = 0; i < sentence.length; i++)
    {
      var punc = "";
      if (sentence[i][0] == '(')
      {
        var ix = sentence[i].indexOf(')');
        punc = sentence[i].substring(ix+1,sentence[i].length);
        sentence[i] = sentence[i].substring(0,ix+1);
        var next = "";
        while (next == "")
        {
          if (corpus[sentence[i]] != null && corpus[sentence[i]].length > 0)
          {
            var randix = Math.floor(Math.random() * corpus[sentence[i]].length);
            next = corpus[sentence[i]][randix];
            if (next == null)
            {
              return false; 
            }
            corpus[sentence[i]] = corpus[sentence[i]].filter(function(x) { return x != next; } );
            //print"from this tweet using " + next);
          }
          else if (tweet_ix < tweets.length)
          {
            AddWordsToCorpus(tweets[tweet_ix].replace(/[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]/g," ").split(' '),corpus,dict);            
            //print"Veiwing new tweet " + tweets[tweet_ix]);
            tweet_ix++;
            continue;
          }
          else
          {
            //print"No response for " + sentence[i]);
            response = "";
            break;
          }
          
          if (used_words.indexOf(next) > -1)
          {
            //print"double used " + next);
            corpus[sentence[i]] = corpus[sentence[i]].filter(function(x) { return x != next; } );
            next = "";
          }
          else
          {
            //print"pushing " + next);
            var coOccured = [];
            var normalizedNext = next;
            var ideasFromNext = dict[next.toLowerCase()];
            for (var w = ideasFromNext.length-1; w >= 0; w--)
            {
              used_words.push(ideasFromNext[w][0]); 
              if (ideasFromNext[w][1][2] == 't' && ideasFromNext[w][1][3] == ')')
              {
                normalizedNext = ideasFromNext[w][0]; 
                //print"normalized = " + normalizedNext);
              }
            }
            var occurances = coOccuranceDict[normalizedNext];
            if (occurances != null)
            {
              //print"occurances = " + occurances);
              for (var w = 0; w < occurances.length; w++)
              {
                for (var u = 0; u < occurances[w][1]; u++)
                {
                  //print"CoOccuring = " + occurances[w][0]);
                  coOccured.push(occurances[w][0]); 
                }
              }
              AddWordsToCorpus(coOccured,corpus,dict);
            }
          }
        }
        if (next == "")
        {
          break; 
        }
        if (last_word_a) // FUCK ENGLISH
        {
          last_word_a = false;
          if (next[0] == 'a' || next[0] == 'e' || next[0] == 'i' || next[0] == 'o')
          {
            response = response + "n";
          }
          response = response + " "; 
        }
        response = response + next + punc + " ";
      }
      else if (sentence[i]=="a" || sentence[i]=="A")
      {
        last_word_a = true;
        response = response + sentence[i];
      }
      else
      {
        response = response + sentence[i] + " "; 
      }
    }
    if (response == "")
    {
      continue; 
    }
    return response;
  }
  return false;
}

function LoadNegativeWords()
{
    return fs.readFileSync(path + "negative.txt",'utf-8').replace(/\n/g," "); 
}
function LoadAllTweets()
{
    return fs.readFileSync(path + "tweets.txt",'utf-8').split("\n").reverse();
}

function getRandomSentence(sentencefile)
{
    var result = fs.readFileSync(path + sentencefile,'utf-8').split("\n"); 
    var theresult = result[Math.floor(Math.random() * result.length)]; 
    return theresult;
}

module.exports = { 
    Insult : function() 
    { 
	response = chooseResponse([LoadNegativeWords()], 30, "Insults.txt");
	console.log(response);
    },
    Respond : function() 
    { 
	response = chooseResponse(LoadAllTweets(), 30, "Phrases.txt");
	console.log(response);
    }
};

