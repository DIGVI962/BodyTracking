using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BodyTracking : MonoBehaviour
{
    public UDPReceive udpreceive;
    public GameObject[] bodypoints;
    
    void Start()
    {
        
    }

    
    void Update()
    {
        string data = udpreceive.data;
        data = data.Remove(0, 1);
        data = data.Remove(data.Length - 1, 1);
        string[] points = data.Split(',');

        for(int i=0; i<33; i++)
        {
            float x = float.Parse(points[i * 3])/100;
            float y = float.Parse(points[i * 3 + 1])/100;
            float z = float.Parse(points[i * 3 + 2])/500;

            bodypoints[i].transform.localPosition = new Vector3(x, y, z);
        }
        
    }
}
