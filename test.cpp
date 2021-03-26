#include <iostream>
using namespace std;    
main()
{    
    for(int i=1;i<101;i++)
    {
        if (i%3==0 && i%5==0)
        {
            cout<<i<<"=3 and 5"<< endl;
        }
        else if(i%3==0)
        {
            cout<<i<<"=3"<< endl;
        }
        else if(i%5==0)
        {
            cout<<i<<"=5"<< endl;
        }
    }    
}