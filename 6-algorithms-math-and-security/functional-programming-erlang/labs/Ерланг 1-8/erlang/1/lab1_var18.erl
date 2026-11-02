-module(lab1_var18).
-export([classify/3, demo/0]).

classify(wine, Years, _Container) when is_integer(Years), Years >= 0, Years < 1 ->
    young;
classify(wine, Years, _Container) when is_integer(Years), Years >= 1, Years < 3 ->
    aged;
classify(wine, Years, _Container) when is_integer(Years), Years >= 3, Years < 5 ->
    reserve;
classify(wine, Years, _Container) when is_integer(Years), Years >= 5 ->
    grand_reserve;


classify(spirit, Years, oak) when is_integer(Years), Years >= 0, Years < 1 ->
    white;          
classify(spirit, Years, oak) when is_integer(Years), Years >= 1, Years < 3 ->
    reposado;       
classify(spirit, Years, oak) when is_integer(Years), Years >= 3, Years < 6 ->
    anejo;
classify(spirit, Years, oak) when is_integer(Years), Years >= 6 ->
    extra_anejo;

classify(spirit, Years, other) when is_integer(Years), Years >= 0, Years < 1 ->
    young_spirit;
classify(spirit, Years, other) when is_integer(Years), Years >= 1 ->
    rested;

classify(Category, Years, Container) ->
    {error, {bad_args, Category, Years, Container}}.

demo() ->
    [
      {wine, 0, other, classify(wine, 0, other)},
      {wine, 2, other, classify(wine, 2, other)},
      {wine, 4, oak,   classify(wine, 4, oak)},
      {spirit, 0, oak, classify(spirit, 0, oak)},
      {spirit, 2, oak, classify(spirit, 2, oak)},
      {spirit, 5, oak, classify(spirit, 5, oak)},
      {spirit, 2, other, classify(spirit, 2, other)}
    ].