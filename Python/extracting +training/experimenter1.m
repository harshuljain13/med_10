
N1=4833;
%L=40:
L=10;
j=1;
%y =y1;
%t = 0:0.0001:0.008;
%y =5*sin(2*pi*50*t)+10*sin(2*2*pi*50*t)+12*sin(3*2*pi*50*t)+20*sin(5*2*pi*50*t);
%T=0.00025;
T=0.08;
y112=k1;
y111=k2;
x111=1:1:N1;
N2=floor(N1/500);
    vk=zeros(10,N2);
    freqk=zeros(10,N2);
    alphak=zeros(10,N2);
    phasek=zeros(10,N2);
    avgk=zeros(2,N2);
    parameters=zeros(13,N2);
    spO2=zeros(1,N2);
    


for num=1:1:N2
    
    N=500;
    
    x=x111((((num-1)*500)+1):(num*500));
    y=y111((((num-1)*500)+1):(num*500));
    y1=y112((((num-1)*500)+1):(num*500));

    suom=0;
    sumi=0;
    acsum=0;
    acsum1=0;
    for p=1:N
        suom=suom+y(p);
        acsum=acsum+y(p)*y(p);
        sumi=sumi+y1(p);
        acsum1=acsum1+y1(p)*y1(p);
    end
    avg=suom/N;
    avg1=sumi/N;

    
    for p=1:N
        y(p)=y(p)-avg;
        y1(p)=y1(p)-avg1;
    end
    for p=1:N
        acsum=acsum+y(p)*y(p);
        acsum1=acsum1+y1(p)*y1(p);
    end
        ac=sqrt(acsum/N);
        ac1=sqrt(acsum1/N);


    plot(x,y+avg,'r');
    hold on;


    order=1;
    fs=12.5;
    [b,a] = butter(order,(5/(fs/2)), 'low');
    y=filter(b,a,y);
    %{
    y=y(1:100);
    x=x(1:100);
    N=10;
    plot(x,y,'c');
    %}
    %formation of d:
    N=500;
    L=10;
    
  d=zeros(1,(N-L));
  j=1;
for i=(L+1):N
d(j)=y(i);
j=j+1;
end


%formation of D:

D=zeros((N-L),L);
r=1;
c=1;
for i=1:(N-L)
for j=1:L
D(r,c)=y(L-j+i);
c=c+1;
end
c=1;
r=r+1;
end
a=pinv(D)*d';
z=roots([1;-a]);

% formation of  y=uc:

%formation of y1=y:

y1=zeros(L,1);
for i=1:L
y1(i)=y(L+i);
end

%formation of u:

u=zeros(L,L);
u=complex(u);
r=1;
c=1;
for i=1:L
for j=1:L
u(r,c)=power(z(j),(r-1));
c=c+1;
end
c=1;
r=r+1;
end
c=u\y1;

%Find amplitude:

val=zeros(1,L);
for i=1:L
val(i)=abs(c(i)*2);
end


v=val';

%Find frequency:

f=zeros(1,L);
for i=1:L
re=real(z(i));
im=imag(z(i));
f(i)=(atan(im/re))/(2*pi*T);
end
freq=f';



for i=1:L
if abs(freq(i))<0.1
v(i)=v(i)/2;
end
end


%Find alpha:

alpha=zeros(1,L);
for i=1:L
alpha(i)=log(abs(z(i)))/T;
end
alpha=alpha';


%find phase angle-phi:

phi=zeros(1,L);

for i=1:L
phi(i)=angle(c(i))*(180/pi);
end
phase=phi';

for i=1:L
    if(freq(i)<0.2)
        v(i)=0;
        freq(i)=0;
        phase(i)=0;
        alpha(i)=0;
    end
end

    for i=1:L
        if(freq(i)<0.2)
            v(i)=0;
            freq(i)=0;
            phase(i)=0;
            alpha(i)=0;
        end
    end

    hasChanged = true;
        itemCount = numel(v);

        while(hasChanged)

            hasChanged = false;
            itemCount = itemCount - 1;

            for index = (1:itemCount)

                if(freq(index) > freq(index+1))
                    v([index index+1]) = v([index+1 index]); %swap v
                    freq([index index+1]) = freq([index+1 index]); %swap freq
                    phase([index index+1]) = phase([index+1 index]); %swap phase
                    alpha([index index+1]) = alpha([index+1 index]); %swap alpha
                    hasChanged = true;
                end %if

            end %for
        end %while


    fprintf('Voltage       Frequency        alpha          phase\n')
    fprintf('...................................................\n')
    for j=1:L
    fprintf('\n %f    %f    %f   %f\n',v(j),freq(j), alpha(j),phase(j));

    end
    fprintf('\n');


    Simulated_Output=zeros(N);


    for i=1:N
       Simulated_Output(i)=Simulated_Output(i)-0.4;
        for j=1:L
            Simulated_Output(i)=Simulated_Output(i)+v(j)*sin(phase(j)+2*pi*freq(j)*i*T);
        end
    end
    plot(x,y+avg);

    hold on;

    plot(x,Simulated_Output+avg,'g');

    stem(freq,v);

    for pp=1:10
        vk(pp,num)=v(pp);
        freqk(pp,num)=freq(pp);
        alphak(pp,num)=alpha(pp);
        phasek(pp,num)=phase(pp);
    end
         avgk(1,num)=avg;
         avgk(2,num)=avg1;
         spO2(num)=(ac1/avg1)/(ac/avg)*100;
    for pas=1:5
        parameters(pas,num)=freqk(5+pas,num);
    end
    for pas=6:10
        parameters(pas,num)=vk(pas,num);
    end
    parameters(11,num)=avg;
    parameters(12,num)=avg1;
    parameters(13,num)=spO2(num);
    
end
