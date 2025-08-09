#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

int main()
{
    int n, m, x, y;
    cin >> n >> m >> x >> y;

    int condition = (x * y + 1) / 2;
    int awakeApartments = 0;

    vector<string> windows(n * x);
    for (int i = 0; i < n * x; i++)
    {
        cin >> windows[i];
    }

    for (int floor = 0; floor < n; floor++)
    {
        for (int apart = 0; apart < m; apart++)
        {
            int litWindows = 0;

            for (int row = 0; row < x; row++)
            {
                string &line = windows[floor * x + row];
                for (int col = apart * y; col < apart * y + y; col++)
                {
                    if (line[col] == 'X')
                    {
                        litWindows++;
                    }
                }
            }
            if (litWindows >= condition)
            {
                awakeApartments++;
            }
        }
    }

    cout << awakeApartments << "\n";

    return 0;
}
