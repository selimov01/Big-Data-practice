#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <tuple>

using namespace std;

const long long INF = 1e15;

int n, m, k, t;
int cost[10][10];
vector<vector<int>> image;

long long dp_seg[51][10][451];
const int MAX_SUM = 9 * 50;

vector<vector<tuple<int, int, long long>>> segments_cache(10);

const vector<tuple<int, int, long long>> &generate_segments(int orig)
{
    if (!segments_cache[orig].empty())
        return segments_cache[orig];

    int target = orig * k;

    for (int pos = 0; pos <= k; pos++)
        for (int last = 0; last < 10; last++)
            for (int sum = 0; sum <= MAX_SUM; sum++)
            {
                dp_seg[pos][last][sum] = INF;
            }

    for (int pix = 0; pix < 10; pix++)
    {
        if (pix <= MAX_SUM)
        {
            dp_seg[0][pix][pix] = 0;
        }
    }

    for (int pos = 0; pos < k - 1; pos++)
    {
        for (int last = 0; last < 10; last++)
        {
            for (int sum = 0; sum <= MAX_SUM; sum++)
            {
                long long cur = dp_seg[pos][last][sum];

                if (cur == INF)
                {
                    continue;
                }

                int rem = k - pos - 1;
                int min_needed = target - sum - 9 * rem;
                int max_needed = target - sum;

                if (max_needed < 0)
                {
                    continue;
                }

                int start_val = max(0, min_needed);
                int end_val = min(9, max_needed);

                for (int next_pix = start_val; next_pix <= end_val; next_pix++)
                {
                    int ns = sum + next_pix;
                    long long penalty = cur + cost[last][next_pix];

                    if (penalty < dp_seg[pos + 1][next_pix][ns])
                        dp_seg[pos + 1][next_pix][ns] = penalty;
                }
            }
        }
    }

    vector<tuple<int, int, long long>> res;

    for (int end = 0; end < 10; end++)
    {
        long long val = dp_seg[k - 1][end][target];
        if (val < INF)
        {
            res.emplace_back(0, end, val);
        }
    }

    segments_cache[orig] = res;
    return segments_cache[orig];
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m >> k;
    image.resize(n, vector<int>(m));

    for (int i = 0; i < n; i++)
    {
        string s;
        cin >> s;

        for (int j = 0; j < m; j++)
        {
            image[i][j] = s[j] - '0';
        }
    }

    cin >> t;
    for (int i = 0; i < 10; i++)
        for (int j = 0; j < 10; j++)
            cost[i][j] = (i - j) * (i - j);

    for (int i = 0; i < t; i++)
    {
        int a, b, c;
        cin >> a >> b >> c;

        cost[a][b] = c;
        cost[b][a] = c;
    }

    long long total_penalty = 0;
    for (int row_idx = 0; row_idx < n; row_idx++)
    {
        const vector<int> &row = image[row_idx];
        vector<long long> dp_line(10, 0);

        for (int i = 0; i < m; i++)
        {
            const auto &segs = generate_segments(row[i]);
            vector<long long> new_dp(10, INF);

            for (int prev_last = 0; prev_last < 10; prev_last++)
            {
                long long base = dp_line[prev_last];

                if (base == INF)
                {
                    continue;
                }

                for (auto &seg : segs)
                {
                    int start, end;
                    long long inside_penalty;
                    tie(start, end, inside_penalty) = seg;
                    long long trans_penalty = (i == 0) ? 0 : cost[prev_last][start];
                    long long val = base + inside_penalty + trans_penalty;

                    if (val < new_dp[end])
                        new_dp[end] = val;
                }
            }
            dp_line = move(new_dp);
        }

        long long row_min = *min_element(dp_line.begin(), dp_line.end());
        total_penalty += row_min;
    }

    cout << total_penalty << "\n";

    return 0;
}