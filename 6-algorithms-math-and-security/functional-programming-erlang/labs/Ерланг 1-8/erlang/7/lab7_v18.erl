-module(lab7_v18).
-export([wear_together/0, db_clothes/0]).

%% {Name, Kind, Season, Weather}


db_clothes() ->
    [
      {tshirt,   top,   summer, hot},
      {shorts,   bottom,summer, hot},
      {sandals,  shoes, summer, hot},
      {cap,      acc,   summer, hot},
	  {longtshirt, top, summer, windy},

      {hoodie,   outer, spring, cool},
      {jeans,    bottom,spring, cool},
      {sneakers, shoes, spring, cool},

      {raincoat, outer, autumn, rainy},
      {umbrella, acc,   autumn, rainy},
      {boots,    shoes, autumn, rainy},

      {coat,     outer, winter, cold},
      {scarf,    acc,   winter, cold},
      {gloves,   acc,   winter, cold}
    ].


wear_together() ->
    DB = db_clothes(),

    Groups0 =
        [{Season, Weather,
          [Name || {Name, _Kind, S, W} <- DB, S == Season, W == Weather]}
         || {_Name, _Kind, Season, Weather} <- DB],

    Groups = del_dbles(Groups0),

    [G || G = {_Season, _Weather, Names} <- Groups, length(Names) >= 2].


del_dbles([{S, W, Names} | T]) ->
    Tclear = del_examples(T, {S, W}),
    [{S, W, Names} | del_dbles(Tclear)];
del_dbles([]) ->
    [].

del_examples([], _Key) ->
    [];
del_examples([{S, W, _Names} | Xs], Key) when {S, W} == Key ->
    del_examples(Xs, Key);
del_examples([X | Xs], Key) ->
    [X | del_examples(Xs, Key)].