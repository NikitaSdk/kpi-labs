-module(lab6_v18).
-export([matrix_main/1, matrix_data/1, swap_center/1]).

matrix_data(1) ->
    [[1,2,3,4,5],
     [6,7,8,9,10],
     [11,12,13,14,15],
     [16,17,18,19,20],
     [21,22,23,24,25]];
matrix_data(2) ->
    [[1,1,1],
     [2,2,2],
     [3,3,3]].


matrix_main(K) ->
    M = matrix_data(K),
    swap_center(M).

swap_center(M) ->
    N = length(M),
    C = (N + 1) div 2,
    RowC = lists:nth(C, M),
    ColC = [lists:nth(C, Row) || Row <- M],
    swap_rows(M, 1, C, RowC, ColC).

swap_rows([Row | Rs], I, C, RowC, ColC) when I =:= C ->
    [ColC | swap_rows(Rs, I + 1, C, RowC, ColC)];
swap_rows([Row | Rs], I, C, RowC, ColC) ->
    NewVal = lists:nth(I, RowC),
    NewRow = replace_nth(C, Row, NewVal),
    [NewRow | swap_rows(Rs, I + 1, C, RowC, ColC)];
swap_rows([], _I, _C, _RowC, _ColC) ->
    [].

replace_nth(1, [_ | T], V) -> [V | T];
replace_nth(Pos, [H | T], V) when Pos > 1 ->
    [H | replace_nth(Pos - 1, T, V)];
replace_nth(_Pos, [], _V) ->
    [].  