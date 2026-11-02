%%cd("D:erl_tests/").

-module(test1).
-export([main1/3]).


%% Задано 2 квадратні матриці Mtr1 nf Mtr2 одного розміру N. 
%% Створити нові 2 матриці, в яких поміняються місцями 
%% (i,j)-тий елемент Mtr1 та  (j,i)-тий елемент Mtr2
%% (1-й індекс - # рядка, 2-й індекс - # стовпчика)

%%%%%%%%%%%%%%%%%%%			% Sequential computing					

%% (N,I,J) ->  {NewMatrix1, NewMatrix2, Time}
main1(N,I,J) ->
%% matrices creation
	Mtr1 = [ [R*K||R <- lists:seq(1, N)] || K <- lists:seq(1, N) ],
	Mtr2 = [ [- R*K||R <- lists:seq(1, N)] || K <- lists:seq(1, N) ],
%% matrices processing
	T1 = erlang:monotonic_time(micro_seconds),
	Mtr1new = new_mtr(Mtr1, I, J, lists:nth(J,lists:nth(I,Mtr2))),
	Mtr2new = new_mtr(Mtr2, J, I, lists:nth(J,lists:nth(I,Mtr1))),	
	io:fwrite("~nMtr1new ~p~n", [Mtr1new]),
	io:fwrite("~nMtr2new ~p~n", [Mtr2new]),	
	T2 = erlang:monotonic_time(micro_seconds),
	T2-T1.

new_mtr([R|Rs], I, J, Xj) when I>1 ->
	[R|new_mtr(Rs, I-1, J, Xj)];
new_mtr([Ri|Rs], 1, J, Xj) ->
	[repl_j_th(Ri,J,Xj)|Rs].

repl_j_th([X|Xs],J,Xj) when J>1 ->
	[X|repl_j_th(Xs,J-1, Xj)];
repl_j_th([_X|Xs],1,Xj) ->
	[Xj|Xs].




	