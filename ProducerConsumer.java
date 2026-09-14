package task;

// Producer Consumer Problem

public class ProducerConsumer {

    // Shared buffer
    static int[] buffer = new int[5];

    static int count = 0;
    static int in = 0;
    static int out = 0;

    // Producer adds items to buffer
    static synchronized void produce(int value) {

        try {

            // Wait if buffer is full
            while (count == 5) {
                wait();
            }

            buffer[in] = value;
            in = (in + 1) % 5;
            count++;

            System.out.println("Produced: " + value);

            // Tell consumer that item is ready
            notifyAll();

        } catch (Exception e) {
            System.out.println(e);
        }
    }

    // Consumer removes items from buffer
    static synchronized void consume() {

        try {

            // Wait if buffer is empty
            while (count == 0) {
                wait();
            }

            int value = buffer[out];
            out = (out + 1) % 5;
            count--;

            System.out.println("Consumed: " + value);

            // Tell producer that space is free
            notifyAll();

        } catch (Exception e) {
            System.out.println(e);
        }
    }

    // Producer thread
    static class Producer extends Thread {

        public void run() {

            for (int i = 1; i <= 10; i++) {

                produce(i);

                try {
                    Thread.sleep(400);
                } catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    // Consumer thread
    static class Consumer extends Thread {

        public void run() {

            for (int i = 1; i <= 10; i++) {

                consume();

                try {
                    Thread.sleep(600);
                } catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    public static void main(String[] args) {

        // Create both threads
        Producer p = new Producer();
        Consumer c = new Consumer();

        // Start the threads
        p.start();
        c.start();
    }
}
