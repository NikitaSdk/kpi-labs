-module(lab4_v18).
-export([task/1]).

%% - взяти 2-й і 5-й елементи початкового списку
%% - видалити передостанній елемент
%% - додати в кінець 2-й і 5-й елементи
task(L) ->
    case length(L) >= 5 of
        false ->
            {error, list_too_short};  
        true ->
            E2 = nth(2, L),
            E5 = nth(5, L),
            L1 = remove_penultimate(L),
            {ok, L1 ++ [E2, E5]}
    end.


nth(1, [X | _]) ->
    X;
nth(N, [_ | T]) when N > 1 ->
    nth(N - 1, T).

remove_penultimate([_Penultimate, Last]) ->
    [Last];
remove_penultimate([H | T]) ->
    [H | remove_penultimate(T)].