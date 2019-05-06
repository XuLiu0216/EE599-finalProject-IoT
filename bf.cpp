#include<iostream>
#include <iterator>
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
#include<map>
#include "loc.h"
#include<set>
using namespace std;
class UserEntity;
class ParkingEntities;
/*class loc{
public:
	int x;
	int y;
	loc(){}
	loc(int x, int y){
		this->x = x;
		this->y = y;
	}
};*/
class Entity 
{
private:
   int id; 
   loc Loc;
   int startTime;
   int endTime;
   
public:
   // int *List;
    virtual void print_result() = 0; 
    int get_id() { return id; } 
    void set_id(int ID){this->id = ID;}
    loc get_loc(){ return Loc;}
    void set_loc(loc location){this->Loc = location;}
    int get_startTime(){ return startTime;}
    void set_startTime(int st){this->startTime = st;}
    int get_endTime(){ return endTime;}
    void set_endTime(int nt){this->endTime = nt;}
    //int* get_list(){ return List;}
    friend class interaction;
};
/*class UserEntity:public Entity{
private:

        //int id;
        //loc currLoc;
        int pref;
        int budget;
        loc destLoc;
        int date;
        //int startTime;
        //int endTime;
        //int* pList;
        //int opt;
public:
        ParkingEntities* pList;
        ParkingEntities opt;
//      int opt_id;
        UserEntity(){}
        UserEntity(int id, loc currLoc, int pref, int budget, loc destLoc, int date,int startTime, int endTime){
                set_id(id);
                //this->currLoc = currLoc;
                set_loc(currLoc);
                this->pref = pref;
                this->budget = budget;
                this->destLoc = destLoc;
                this->date = date;
                set_startTime(startTime);
                set_endTime(endTime);
                //this->opt = -1;
        }
        ParkingEntities get_opt(){return opt;}
        loc get_destLoc(){return destLoc;}
        int get_pref(){return pref;}
        int get_date(){return date;}
        void print_result(){
                cout << "User id: " << get_id() <<", "<< "opt " << get_opt().get_id() << endl;
        }
	friend class ParkingEntities;

};
 */
class ParkingEntities:public Entity{
private:        
	//int id;
        //loc location;
        int charge;
        int maxTime;
        int workday;
        //int startTime;
        //int endTime;
        int numSpot;
        int count;
	//UserEntity& u;
        //int* uList;
public:
	 ParkingEntities(){}
        ParkingEntities(int id,loc loca, int charge, int maxTime,int workday, int startTime, int endTime, int numSpot){
        set_id(id);
        //this->location = loca;
	set_loc(loca);
        this->charge = charge;
        this->maxTime = maxTime;
        this->workday = workday;
        set_startTime(startTime);
        set_endTime ( endTime);
        this->numSpot = numSpot;
        this->count = 0;
        }
   	int get_charge(){return charge;}
	int get_maxTime(){return maxTime;}
	int get_workday(){return workday;}
	int get_numSpot(){return numSpot;}
	int get_count(){return count;} 
	void print_result(){
		cout << "Parking id: " << get_id() << ", " << "has " << get_numSpot() << "spots" << endl;
}
/*      int get_cost(UserEntity u){
                int hour = charge/100;
                int day = charge%100;
                if(hour == 0){
                        return day;
                }
                else if(day == 0){
                        return hour;
                }
                else{
                        if(day < hour*(u.get_endTime()-u.get_startTime())){
                                return day;
                        }
                        else{
                                return hour*(u.get_endTime()-u.get_startTime());
                        }
                }
        }*/
friend class interaction;
	
};

class UserEntity:public Entity{
private:

        //int id;
        //loc currLoc;
        int pref;
        int budget;
        loc destLoc;
        int date;
	double drivetime;
	double walktime;
        //int startTime;
        //int endTime;
        //int* pList;
        //int opt;
public:
        ParkingEntities* pList;
        set<int> near;
        ParkingEntities opt;
//      int opt_id;
        UserEntity():drivetime(INT_MAX-0.00),walktime(INT_MAX-0.00){}
        UserEntity(int id, loc currLoc, int pref, int budget, loc destLoc, int date,int startTime, int endTime){
                set_id(id);
                //this->currLoc = currLoc;
                set_loc(currLoc);
                this->pref = pref;
                this->budget = budget;
                this->destLoc = destLoc;
                this->date = date;
                set_startTime(startTime);
                set_endTime(endTime);
                //this->opt = -1;
        }
        ParkingEntities get_opt(){return opt;}
        loc get_destLoc(){return destLoc;}
        int get_pref(){return pref;}
        int get_date(){return date;}
	double get_walk(){return walktime;}
	double get_drive(){return drivetime;}
        void print_result(){
                cout << "User id: " << get_id() <<", "<< "opt " << get_opt().get_id() << endl;
        }
        friend class interaction;

};

vector<UserEntity> U;
vector<ParkingEntities> P;
map<int, ParkingEntities> pmap;
class interaction{
public:
UserEntity* u;
ParkingEntities* p;
interaction(UserEntity* in_u,ParkingEntities* in_p){this->u = in_u;this->p = in_p;}
int get_cost(){
                int hour =(*p).charge/100;
                int day = (*p).charge%100;
                if(hour == 0){
                        return day;
                }
                else if(day == 0){
                        return hour;
                }
                else{
                        if(day < hour*((*u).endTime-(*u).startTime)){
                                return day;
                        }
                        else{
                                return hour*((*u).endTime-(*u).startTime);
                        }
                }
        }
bool check(){
	if((*p).numSpot > 0){
	if((*u).startTime >= (*p).startTime && (*u).endTime <= (*p).endTime && (*u).endTime - (*u).startTime <(*p).maxTime){
                    if(get_cost() <= (*u).budget){
                        return true;
			}
	}
	}
            return false;
}

void searchParkingWithin(int meters){
  //  vector<ParkingEntities> res;
    (*u).near.clear();
    double dis;
    ParkingEntities p;
    for (int i = 0; i < P.size(); i++){
        p = P[i];
        dis = sqrt(pow(((*u).destLoc.x - p.Loc.x),2) +pow(((*u).destLoc.y - p.Loc.y),2));
        if (dis <= meters){
            //res.push_back(p);
		(*u).near.insert(p.id);
	
        }

}
}
void get_driving_time(){
    srand(time(NULL));
    int speed = rand()%45+15;
    double dis = sqrt(pow(((*u).Loc.x - (*p).Loc.x), 2) +pow( ((*u).Loc.y - (*p).Loc.y), 2));
    double time = ((dis / speed) / 1000 )* 60;
    (*u).drivetime= time;
}


void get_walking_time(){
    //assume walking speed 4500 meters/h
    (*u).walktime =   (sqrt(pow(((*p).Loc.x - (*u).destLoc.x), 2) +pow(((*p).Loc.y -(*u).destLoc.y), 2))/4500)*60;
}

};


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
		//U.insert(user);
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
	//P.insert(parking);
   pmap.insert(pair<int, ParkingEntities>(id, parking)); 
}
}
vector<ParkingEntities> searchParkingWithin(loc destLoc,vector<ParkingEntities> Pk, int meters){
    vector<ParkingEntities> res;
    double dis;
        ParkingEntities p;
	//set<ParkingEntities>::iterator it;
   // for(it=Pk.begin();it!=Pk.end();it++){
    for (int i = 0; i < Pk.size(); i++){
        p = Pk[i];
        dis = sqrt(pow((destLoc.x - p.get_loc().x),2) +pow((destLoc.y - p.get_loc().y),2));
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
    return  (sqrt(pow((loc1.x - loc2.x), 2) +pow((loc1.y - loc2.y), 2))/4500)*60;
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
      // set<ParkingEntities>::iterator it;
      //for(it=U.begin();it!=U.end();it++){  
	interaction one = interaction(& U[i], &p);
        one.searchParkingWithin(meters); 
	set <int > :: iterator itr; 
	for(itr = U[i].near.begin(); itr!= U[i].near.end(); itr++){
		int id = *itr;
		ParkingEntities p2 =  pmap.find(id)->second;
		interaction two = interaction(&U[i],& p2);
		if(!two.check()){
			U[i].near.erase(id);
			continue;
		}
	}
        //vector<ParkingEntities> P2 = searchParkingWithin(U[i].get_destLoc(), P, meters);
        min_value = INT_MAX-0.00;
        min_id = -1;
        //for(int j = 0; j < P2.size(); j++){
	 for(itr = U[i].near.begin(); itr!= U[i].near.end(); itr++){
            //p = P2[j];
            //t1 = get_driving_time(U[i].get_loc(), p.get_loc());
            //t2 = get_walking_time(p.get_loc(), U[i].get_destLoc());
            //t = t1 + t2;
		 int id = *itr;
                ParkingEntities p3 =  pmap.find(id)->second;
	    interaction three = interaction(&U[i],& p3);
		three.get_walking_time();
		three.get_driving_time();
           // if (t < min_value){
		if(U[i].get_walk()+U[i].get_drive() < min_value){
                min_value = U[i].get_walk()+U[i].get_drive();
                //min_id = p.get_id();
		min_id = id;
		}
	}
	//cout << min_id << endl;
        U[i].opt = pmap.find(min_id)->second;
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
// set<ParkingEntities>::iterator it;
 for(int i = 0; i < U.size();i++){
// for(it=U.begin();it!=U.end();it++){   
 //cout <<i<<"th user's opt: "<< U[i].opt << endl;
  U[i].print_result();
}

	return 0;
}
