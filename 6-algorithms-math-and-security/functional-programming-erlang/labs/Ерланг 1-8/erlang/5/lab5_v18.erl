-module(lab5_v18).
-export([list_pro_main1/1, list_pro_main2/1]).

%% split
list_pro_main1(L) ->
    K = length(L) div 4,
    {Q1, Rest1} = lists:split(K, L),
    {Q2, Rest2} = lists:split(K, Rest1),
    {Q3, _Q4}   = lists:split(K, Rest2),
    lists:reverse(Q1) ++ Q2 ++ Q3.
	
%% one pass 
list_pro_main2(L) ->
    K = length(L) div 4,
    list_pro(L, 1, K, 3*K, [], []).  

list_pro([X|Xs], I, K, Limit, AccQ1Rev, AccRestRev) when I =< K ->
    list_pro(Xs, I+1, K, Limit, [X|AccQ1Rev], AccRestRev);

list_pro([X|Xs], I, K, Limit, AccQ1Rev, AccRestRev) when I =< Limit ->
    list_pro(Xs, I+1, K, Limit, AccQ1Rev, [X|AccRestRev]);

list_pro(_Rest, _I, _K, _Limit, AccQ1Rev, AccRestRev) ->
    AccQ1Rev ++ lists:reverse(AccRestRev).