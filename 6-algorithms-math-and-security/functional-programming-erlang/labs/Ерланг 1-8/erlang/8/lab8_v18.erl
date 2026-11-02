-module(lab8_v18).
-export([count1/2, count2/2, count3/2, count4/2]).

%% 1) Guard + pattern matching
count1(Pattern, [X|Xs]) when X =:= Pattern ->
    1 + count1(Pattern, Xs);
count1(Pattern, [_X|Xs]) ->
    count1(Pattern, Xs);
count1(_Pattern, []) ->
    0.

%% 2) Через case
count2(Pattern, [X|Xs]) ->
    case X =:= Pattern of
        true  -> 1 + count2(Pattern, Xs);
        false -> count2(Pattern, Xs)
    end;
count2(_Pattern, []) ->
    0.

%% 3) Через BIF lists:filter/2
count3(Pattern, List) ->
    length(lists:filter(fun(X) -> X =:= Pattern end, List)).

%% 4) Через генератор списку
count4(Pattern, List) ->
    length([X || X <- List, X =:= Pattern]).