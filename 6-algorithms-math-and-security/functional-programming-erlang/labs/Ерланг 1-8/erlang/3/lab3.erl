-module(lab3).
-export([func_main/4, func_list/4, sum_tail/3]).

%% func_main(X, Xfinal, Step, N) 
func_main(X, Xf, H, N) ->
    func_list(X, Xf + H/100, H, N).

func_list(X, Xf, H, N) when X =< Xf ->
    [sum_tail(X, N, 0.0) | func_list(X + H, Xf, H, N)];
func_list(X, Xf, _H, _N) when X > Xf ->
    [].

sum_tail(X, N, Acc) ->
    sum_tail(X, N, N, Acc).
	
%% sum_tail(X, I, Nconst, Acc)
sum_tail(X, 0, Nconst, Acc) ->
    Den = X + Nconst,
    case Den of
        0.0 -> {error, division_by_zero};
        _   -> Acc / Den
    end;
sum_tail(X, I, Nconst, Acc) when I > 0 ->
    Term = math:pow(X, I) + Nconst,
    sum_tail(X, I - 1, Nconst, Acc + Term).