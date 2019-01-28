FROM alpine:latest
MAINTAINER Mikael Kall <nighter@nighter.se>

ENV ROOT_PASSWORD root

RUN set -x \
  && apk update 

RUN apk --update add openssh \
		&& sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
		&& sed -i 's/#Port 22/Port 80/' /etc/ssh/sshd_config \
        && echo "root:${ROOT_PASSWORD}" | chpasswd \
		&& rm -rf /var/cache/apk/* /tmp/* \
                && /usr/bin/ssh-keygen -A

RUN sed -i 's#root:x:0:0:root:/root:/bin/ash#root:x:0:0:root:/root:/bin/true#g' /etc/passwd

COPY entrypoint.sh /usr/local/bin/

EXPOSE 80

CMD ["/usr/local/bin/entrypoint.sh"]
