#include<iostream>
#include<fstream>
#include<string>
#include<math.h>
#include <vector> 
#include<stdio.h>
#include <stdlib.h>
#include<cstdlib>
#include<bits/stdc++.h> 
#include <cmath>
#include <ctime>
using namespace std;
class loc{
public:
	int x;
	int y;
	loc(){}
	loc(int x, int y){
		this->x = x;
		this->y = y;
	}
};
class UserEntity{
public:
	
	int id;
	loc currLoc;
	int pref;
	int budget;
	loc destLoc;
	int date;
	int startTime;
	int endTime;
	int* pList;
	int opt;
	UserEntity(){}
	UserEntity(int id, loc currLoc, int pref, int budget, loc destLoc, int date,int startTime, int endTime){
		this->id = id;
		this->currLoc = currLoc;
		this->pref = pref;
		this->budget = budget;
		this->destLoc = destLoc;
		this->date = date;
		this->startTime = startTime;
		this->endTime = endTime;
		this->opt = -1;
	}
};
class ParkingEntities{
public:        
	int id;
        loc location;
        int charge;
        int maxTime;
        int workday;
        int startTime;
        int endTime;
        int numSpot;
        int count;
        int* uList;
	 ParkingEntities(){}
        ParkingEntities(int id,loc loca, int charge, int maxTime,int workday, int startTime, int endTime, int numSpot){
        this->id = id;
        this->location = loca;
        this->charge = charge;
        this->maxTime = maxTime;
        this->workday = workday;
        this->startTime = startTime;
        this->endTime = endTime;
        this->numSpot = numSpot;
        this->count = 0;
        }
};
vector<UserEntity> U;
vector<ParkingEntities> P;
void read_user_input(istream & infile){
    
        string line;
        while(getline(infile,line)){
            int id = atoi((line.substr(0,4)).c_str());
            int userX = atoi((line.substr(4,4)).c_str());
            int userY = atoi((line.substr(8,4)).c_str());
            loc userLoc = loc(userX, userY);
            int destX = atoi((line.substr(12,4)).c_str());
            int destY = atoi((line.substr(16,4)).c_str());
            loc destLoc = loc(destX, destY);
            int pref = atoi((line.substr(20,1)).c_str());
            int budget = atoi((line.substr(20,2)).c_str());
            int date = atoi((line.substr(22,8)).c_str());
            int start = atoi((line.substr(30,2)).c_str());
            int end = atoi((line.substr(32,2)).c_str());
            UserEntity user = UserEntity(id, userLoc,pref,budget, destLoc, date, start, end);
            U.push_back(user);
           }
}
void read_parking_input(istream & infile){
    	string line;
        while(getline(infile,line)){
            int id = atoi((line.substr(0,4)).c_str());
            int parkingX = atoi((line.substr(4,4)).c_str());
            int parkingY = atoi((line.substr(8,4)).c_str());
            loc parkingLoc = loc(parkingX, parkingY);
            int charge = atoi((line.substr(12,4)).c_str());
            int maxtime = atoi((line.substr(16,2)).c_str());
            int workday = atoi((line.substr(18,7)).c_str());
            int start = atoi((line.substr(25,2)).c_str());
            int end = atoi((line.substr(27,2)).c_str());
            int numSpot = atoi((line.substr(29,4)).c_str());
            
            ParkingEntities parking = ParkingEntities(id, parkingLoc, charge, maxtime, workday, start, end, numSpot);
   P.push_back(parking);
}
}
vector<ParkingEntities> searchParkingWithin(loc destLoc,vector<ParkingEntities> Pk, int meters){
    vector<ParkingEntities> res;
    double dis;
        ParkingEntities p;
    for (int i = 0; i < Pk.size(); i++){
        p = Pk[i];
        dis = sqrt(pow((destLoc.x - p.location.x),2) +pow((destLoc.y - p.location.y),2));
        if (dis <= meters){
            res.push_back(p);
        }
       
}
return res;
}
double get_driving_time(loc loc1, loc loc2){
    srand(time(NULL));
    int speed = rand()%45+15;
    double dis = sqrt(pow((loc1.x - loc2.x), 2) +pow( (loc1.y - loc2.y), 2));
    double time = ((dis / speed) / 1000 )* 60;
    return time;
}


double get_walking_time(loc loc1,loc loc2){
    //assume walking speed 4500 meters/h
    int speed = 4500;
    double dis = sqrt(pow((loc1.x - loc2.x), 2) +pow((loc1.y - loc2.y), 2));
    //measured by minitue
    double time = (dis / speed) * 60;
    return time;
}

void bruteforce(){
	double min_value;
	int min_id;
	double t1;
	double t2;
	double t;
//	UserEntity u;
	ParkingEntities p;
	int meters = 2000;
    for(int i = 0; i < U.size(); i++){
        
        vector<ParkingEntities> P2 = searchParkingWithin(U[i].destLoc, P, meters);
        min_value = INT_MAX-0.00;
        min_id = -1;
        for(int j = 0; j < P2.size(); j++){
            p = P2[j];
            t1 = get_driving_time(U[i].currLoc, p.location);
            t2 = get_walking_time(p.location, U[i].destLoc);
            t = t1 + t2;
//	    cout << t << endl;
            if (t < min_value){
                min_value = t;
                min_id = p.id;
		}
	}
	//cout << min_id << endl;
        U[i].opt = min_id;
}
}
	

int main(){
	ifstream infile;
	infile.open("inputUser.txt");
	read_user_input(infile);
	infile.close();
        infile.open("inputParking.txt");
	read_parking_input(infile);
        infile.close();
	//loc location_cur =  loc(1,3);
	//loc location_dest = loc(4,5);
	//UserEntity U = UserEntity(1,location_cur,0,10,location_dest,20190429,1030,1050);
	//U.pList = new int[5];
	//for(int i = 0; i<5; i++){
	//	U.pList[i] = i;
	//}
/*	for(int i = 0; i < U.size(); i++){
	
	cout << "id: " << U[i].id << "\n" << "curLoc: " << U[i].currLoc.x << "," << U[i].currLoc.y << "\n" << "pref: " << U[i].pref << "\n" << "budget: " << U[i].budget << "\n" << "destloc : " << U[i].destLoc.x << U[i].destLoc.y << "\n" << "Date: " << U[i].date << "\n" << "start,end time: " << U[i].startTime << "," << U[i].endTime << "\n" << "opt: " << U[i].opt<<endl;
//	for(int i = 0; i < 5; i++){
//	cout  << U.pList[i] << " " ;
//}
cout << endl;
}
        for(int i = 0; i < P.size(); i++){

        cout << "id: " << P[i].id << "\n" << "location: " << P[i].location.x << "," << P[i].location.y << "\n" << "charge: " << P[i].charge << "\n" << "maxtime: " << P[i].maxTime << "\n" << "workday : " << P[i].workday << "\n"  << "start,end time: " << P[i].startTime << "," << P[i].endTime << "\n" << "num: " << P[i].numSpot<<endl;
//      for(int i = 0; i < 5; i++){
//      cout  << U.pList[i] << " " ;
//}
cout << endl;
}
*/
bruteforce();
//vector<ParkingEntities> res = searchParkingWithin(U[0].destLoc,P,2000);
 for(int i = 0; i < U.size();i++){
  cout << U[i].opt << endl;
}

	return 0;
}
