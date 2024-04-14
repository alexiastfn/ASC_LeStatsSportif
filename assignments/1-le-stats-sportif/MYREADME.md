Stefan Alexia
332CB

# Tema1 - ASC - Le Stats Sportif

## routes.py
- pentru fiecare request, adaug in coada thread pool-ului un task corespunzator si scriu 2 loguri de informare ([START] si [END])
- la get_results am un caz unde am considerat ca logul ar fi de tip warning (cand threadpool.requests_dict este None) si de tip exception cand
inca nu s-a terminat de scris fisierul de output (si am JSONDecodeError)


## task_runner.py

    #### TypeRequest(Task)
    - fiecare tip de task mosteneste clasa Task
    - variabila membru request_map o folosesc pt exerctiul cu get_results
        -> daca request_map[job_id] = None => ar fi trebuit sa dea "Invalid job Id", dar dintr-un motiv sau altul
        checker-ul de pe Moodle nu este de acord, asa ca il consider "running";
        request_map[job_id] = True -> inseamna ca este un job terminat
        request_map[job_id] = False -> inseamna ca este un job in running (se scrie in fisier)
    
        -> am un mutex pentru a evit race condition-ul cand se completeaza requests_map-ul
    - fiecare clasa care mosteneste Task o sa aiba 2 functii:
        -> helper(): unde manipulez dictionarul, care a reiesit din fisierul csv, adaptat pt fiecare tip de request
        -> "execute(): apelez helper, scriu in fisierul de output, actualizez acces_requests_dict cu True si dau un log de informare ([MIDDLE])
    - mai am un request special, care nu era in cerinta temei, numit StopRequest, pe care il adaug in coada threadpool-ului cand stiu ca vreau sa inchid

    #### TaskRunner(Thread)
    - blueprint-ul thread-urilor
    - in run evit busy waiting-ul prin faptul ca self.q este de tip Queue
        -> din documentatie: Queue.get(block=True, timeout=None): Remove and return an item from the queue. If optional args block is true and timeout is None (the default),
        **block if necessary until an item is available**.

    #### ThreadPool
    - getNoThreads(): dupa cum era explic si in schelete, verific daca var TP_NUM_OF_THREADS este definita, daca nu apelez os.cpu_count() pt a mi-da nr de core-uri ale laptop-ului meu
    - stop(): ca sa opresc => trimit no_threads semnale de oprire pt fiecare thread, apoi fac join


### logger.py
- aici imi creez o variabila constanta server_logger ca sa o pot folosi pentru tot unde am nevoie de loguri
- updateLoggerDirectory(): daca folder-ul de loguri exista => il sterg, apoi creez altul
- formatter(): imi formateaza efectiv cum sa arate logurile

### my_unittest.py
- cea mai fun parte din tema
- pt fiecare tip de request am un test
- verific daca output-ul return de functia helper() (din fiecare TypeRequest(Task)) este aproape identic (delta=0.01) cu cel dat in /tests, fara a porni server-ul







