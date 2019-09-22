package tool.testmin.util;

import tool.testmin.Main;

import java.util.concurrent.ThreadFactory;

public class MyThreadFactory implements ThreadFactory {

    public Thread newThread(Runnable r) {
        return new Thread(r, Main.curFile);
    }

}
