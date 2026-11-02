%%cd("D:erl_tests/").

-module(test2).
-export([main2/3]).


%% Задано 2 квадратні матриці Mtr1 nf Mtr2 одного розміру N. 
%% Створити нові 2 матриці, в яких поміняються місцями 
%% (i,j)-тий елемент Mtr1 та  (j,i)-тий елемент Mtr2
%% (1 - # рядка, 2 - # стовпчика)

%%%%%%%%%%%%%%%%%%%			Concurrent  computing

%% (N,I,J) ->  {NewMatrix1, NewMatrix2}
main2(N,I,J) ->
%% matrices creation
	Mtr1 = [ [R*K||R <- lists:seq(1, N)] || K <- lists:seq(1, N) ],
	Mtr2 = [ [- R*K||R <- lists:seq(1, N)] || K <- lists:seq(1, N) ],
%% matrices processing
	T1 = erlang:monotonic_time(micro_seconds),
	PidParent = self(),
	PidMtr2 = spawn(fun () ->
					  	Mtr2new = new_mtr(Mtr2, J, I, PidParent, x_from_Mtr1, x_from_Mtr2),
					  	io:fwrite("~nMtr2new ~p~n", [Mtr2new])
					end),
	Mtr1new = new_mtr(Mtr1, I, J, PidMtr2, x_from_Mtr2, x_from_Mtr1),
	io:fwrite("~nMtr1new ~p~n", [Mtr1new]),
	T2 = erlang:monotonic_time(micro_seconds),
	T2-T1.

%% (Matrix, I, J, Pid, TagFrom, TagTo) -> NewMatrix
new_mtr([R|Rs], I, J, Pid, TagFrom, TagTo) when I>1 ->
	[R|new_mtr(Rs, I-1, J, Pid, TagFrom, TagTo)];
new_mtr([Ri|Rs], 1, J, Pid, TagFrom, TagTo) ->
	[repl_j_th(Ri,J,Pid, TagFrom, TagTo)|Rs].

repl_j_th([X|Xs],J,Pid, TagFrom, TagTo) when J>1 ->
	[X|repl_j_th(Xs,J-1, Pid, TagFrom, TagTo)];
repl_j_th([Xj|Xs],1,Pid, TagFrom, TagTo) ->
	Pid ! {TagTo, Xj},
	receive
		{TagFrom, Xnew} -> Xnew
	end,
	[Xnew|Xs].







	