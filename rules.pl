% Regola per identificare le notizie sospette
detect_suspicious_political_news(Id) :- 
    news(Id, _, Subject, _, NumWords),        % La notizia ha un id, un subject e un numero di parole
    member(Subject, ["politics","politicsNews"]),  % Il subject deve essere 'politics' o 'politicsNews'
    NumWords > 500.                           % Il numero di parole deve essere maggiore di 500


% Lista di parole chiave clickbait
clickbait_keywords([
    "shocking", "incredible", "you won't believe", "unbelievable", 
    "revealed", "exposed", "this will change everything", "what happened next", 
    "the truth about", "secret", "trump", "donald", "vaccine", "covid19", "COVID19"
]).


% Regola per identificare notizie sospette per clickbait
detect_suspicious_clickbait(Id) :-
    news(Id, Text, _, _, _),
    clickbait_keywords(Keywords),
    member(Keyword, Keywords),
    sub_string(Text, _, _, _, Keyword).


% Regola che combina le regole detect_suspicious_clickbait(Id) e detect_suspicious_political_news(Id)
% Che si avvera se una notizia contiene parole clickbait ed è una notizia di politica sospetta
very_suspicious_news(Id) :-
    detect_suspicious_political_news(Id),
    detect_suspicious_clickbait(Id).