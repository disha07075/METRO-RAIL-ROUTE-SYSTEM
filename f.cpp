#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <string>
#include <windows.h>
#include <iomanip>
using namespace std;

class MetroSystem {
    vector<string> stationNames;
    vector<vector<pair<int, int>>> adjList;
    float farePerMinute = 2.0f;

public:
    MetroSystem(int numStations) {
        stationNames.resize(numStations);
        adjList.resize(numStations);
    }

    void addStation(int id, const string& name) {
        if (id >= (int)stationNames.size()) {
            stationNames.resize(id + 1);
            adjList.resize(id + 1);
        }
        stationNames[id] = name;
    }

    void addConnection(int from, int to, int time) {
        adjList[from].push_back({to, time});
        adjList[to].push_back({from, time});
    }

    void setColor(int color) {
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
    }

    void displayGUI() {
        system("cls");
        setColor(11);
        cout << "==============================\n";
        cout << "     DELHI METRO PLANNER      \n";
        cout << "==============================\n";
        setColor(15);
    }

    void showStations() {
        cout << "\nList of Delhi Metro Stations:\n";
        for (int i = 0; i < (int)stationNames.size(); ++i) {
            setColor(14);
            cout << "[" << i << "]";
            setColor(15);
            cout << " " << stationNames[i] << "\n";
        }
    }

    string getStationName(int id) {
        if (id >= 0 && id < (int)stationNames.size()) {
            return stationNames[id];
        }
        return "";
    }

    void showRoute(int start, int end) {
        int n = stationNames.size();
        vector<int> dist(n, INT_MAX);
        vector<int> parent(n, -1);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;

        dist[start] = 0;
        pq.push({0, start});

        while (!pq.empty()) {
            pair<int, int> top = pq.top(); 
            pq.pop();
            int cd = top.first;
            int u = top.second;

            if (cd > dist[u]) continue;

            for (auto& edge : adjList[u]) {
                int v = edge.first;
                int w = edge.second;

                if (cd + w < dist[v]) {
                    dist[v] = cd + w;
                    parent[v] = u;
                    pq.push({dist[v], v});
                }
            }
        }

        if (dist[end] == INT_MAX) {
            setColor(12);
            cout << "\nNo route found between " << stationNames[start] << " and " << stationNames[end] << ".\n";
            setColor(15);
            return;
        }

        vector<int> path;
        for (int v = end; v != -1; v = parent[v])
            path.insert(path.begin(), v);

        setColor(14);
        cout << "\nShortest Route from " << stationNames[start] << " to " << stationNames[end] << ":\n";
        setColor(10);
        for (int i = 0; i < (int)path.size(); ++i) {
            cout << stationNames[path[i]];
            if (i != (int)path.size() - 1) cout << " -> ";
        }

        int totalTime = dist[end];
        float fare = totalTime * farePerMinute;
        setColor(15);
        cout << "\n\nTotal Travel Time: " << totalTime << " minutes";
        cout << "\nFare: ₹" << fixed << setprecision(2) << fare << "\n";
    }

    float getFarePerMinute() const {
        return farePerMinute;
    }

    void setFarePerMinute(float newFare) {
        if (newFare > 0) {
            farePerMinute = newFare;
        } else {
            cout << "Fare must be positive! Keeping previous fare.\n";
        }
    }
};

int main() {
    MetroSystem metro(20);

    metro.addStation(0, "Rajiv Chowk");
    metro.addStation(1, "Kashmere Gate");
    metro.addStation(2, "Central Secretariat");
    metro.addStation(3, "New Delhi");
    metro.addStation(4, "Chandni Chowk");
    metro.addStation(5, "AIIMS");
    metro.addStation(6, "INA");
    metro.addStation(7, "Hauz Khas");
    metro.addStation(8, "Saket");
    metro.addStation(9, "Malviya Nagar");
    metro.addStation(10, "Lajpat Nagar");
    metro.addStation(11, "Moolchand");
    metro.addStation(12, "Nehru Place");
    metro.addStation(13, "Kalkaji Mandir");
    metro.addStation(14, "Govindpuri");
    metro.addStation(15, "Okhla");
    metro.addStation(16, "Jasola");
    metro.addStation(17, "Sarita Vihar");
    metro.addStation(18, "Mohan Estate");
    metro.addStation(19, "Badarpur Border");

    metro.addConnection(0, 1, 4);
    metro.addConnection(1, 2, 5);
    metro.addConnection(2, 3, 3);
    metro.addConnection(3, 4, 6);
    metro.addConnection(4, 5, 4);
    metro.addConnection(5, 6, 7);
    metro.addConnection(6, 7, 5);
    metro.addConnection(7, 8, 6);
    metro.addConnection(8, 9, 4);
    metro.addConnection(9, 10, 5);
    metro.addConnection(10, 11, 8);
    metro.addConnection(11, 12, 5);
    metro.addConnection(12, 13, 3);
    metro.addConnection(13, 14, 6);
    metro.addConnection(14, 15, 4);
    metro.addConnection(15, 16, 5);
    metro.addConnection(16, 17, 6);
    metro.addConnection(17, 18, 4);
    metro.addConnection(18, 19, 7);

    metro.displayGUI();
    metro.setColor(11);
    cout << "\nWelcome to the Delhi Metro Route Planner!\n";
    metro.setColor(15);

    int choice;
    do {
        metro.displayGUI();
        cout << "What would you like to do today?\n";
        cout << "1. See all metro stations\n";
        cout << "2. Find the shortest route between two stations\n";
        cout << "3. View or update fare rate\n";
        cout << "4. Exit the planner\n";
        cout << "Please enter your choice (1-4): ";
        cin >> choice;

        if (choice == 1) {
            metro.showStations();
            cout << "\nDid you find your station? (y/n): ";
            char ans; cin >> ans;
            if (ans == 'n' || ans == 'N') {
                cout << "Exiting the program as per your response.\n";
                break; // Exit program if user doesn't find station
            }
            system("pause");
        } 
        else if (choice == 2) {
            int start, end;
            metro.showStations();
            
            cout << "\nEnter the ID of your starting station: ";
            cin >> start;
            cout << "Enter the ID of your destination station: ";
            cin >> end;

            if (start < 0 || start >= 20 || end < 0 || end >= 20) {
                metro.setColor(12);
                cout << "Oops! One or both station IDs are invalid. Please try again.\n";
                metro.setColor(15);
            } 
            else if (start == end) {
                metro.setColor(13);
                cout << "Start and destination stations are the same! Try different stations.\n";
                metro.setColor(15);
            } 
            else {
                cout << "\nYou chose:\n";
                cout << "Start Station: " << metro.getStationName(start) << "\n";
                cout << "Destination Station: " << metro.getStationName(end) << "\n";

                cout << "Shall I find the shortest route for you? (y/n): ";
                char confirm; cin >> confirm;
                if (confirm == 'y' || confirm == 'Y') {
                    metro.showRoute(start, end);
                }
            }
            cout << "\nWould you like to do something else? (y/n): ";
            char repeat; cin >> repeat;
            if (repeat == 'n' || repeat == 'N') {
                choice = 4;
            }
            system("pause");
        } 
        else if (choice == 3) {
            metro.displayGUI();
            cout << "\nCurrent fare rate is ₹" << metro.getFarePerMinute() << " per minute.\n";
            cout << "Do you want to update the fare rate? (y/n): ";
            char updateFare; cin >> updateFare;
            if (updateFare == 'y' || updateFare == 'Y') {
                float newFare;
                cout << "Enter new fare rate (₹ per minute): ";
                cin >> newFare;
                metro.setFarePerMinute(newFare);
                cout << "Fare updated successfully to ₹" << metro.getFarePerMinute() << " per minute.\n";
            }
            cout << "\nWould you like to do something else? (y/n): ";
            char repeat; cin >> repeat;
            if (repeat == 'n' || repeat == 'N') {
                choice = 4;
            }
            system("pause");
        }
        else if (choice == 4) {
            cout << "Thank you for using Delhi Metro Route Planner. Have a great day!\n";
            break;
        } 
        else {
            metro.setColor(12);
            cout << "Invalid choice! Please enter 1, 2, 3, or 4.\n";
            metro.setColor(15);
            system("pause");
        }
    } while (choice != 4);

    return 0;
}
