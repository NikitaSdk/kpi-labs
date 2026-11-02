-module(lab2_v18).
-export([f_guard/2, f_if/2, factorial/1]).

%% f(x) = k,  якщо 1 < x < k
%% f(x) = x!, якщо x > k

%% guards
f_guard(X, K) when is_integer(X), is_integer(K), X > 1, X < K ->
    K;
f_guard(X, K) when is_integer(X), is_integer(K), X > K, X >= 0 ->
    factorial(X);
f_guard(_X, _K) ->
    {error, out_of_domain}.

%% if
f_if(X, K) when is_integer(X), is_integer(K), X >= 0 ->
    if
        X > 1, X < K ->
            K;
        X > K ->
            factorial(X);
        true ->
            {error, out_of_domain}
    end;
f_if(_X, _K) ->
    {error, bad_args}.

factorial(N) when is_integer(N), N >= 0 ->
    factorial_tail(N, 1);
factorial(_N) ->
    {error, bad_factorial_arg}.

factorial_tail(0, Acc) ->
    Acc;
factorial_tail(N, Acc) when N > 0 ->
    factorial_tail(N - 1, Acc * N).