from datetime import datetime

import requests
from django.db.models import Value, Count, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DeleteView
from rest_framework.response import Response
from rest_framework.views import APIView


import neulhaerang_review
from member.models import Member
from neulhaerang.models import Neulhaerang, NeulhaerangReply, MemberByeoljji, Byeoljji, NeulhaerangDonation
from neulhaerang_review.models import NeulhaerangReviewReply, NeulhaerangReview
from neulhajang.models import Neulhajang, NeulhajangAuthenticationFeed
from static_app.models import Badge, MemberBadge
from workspace.pagenation import Pagenation
from workspace.serializers import PagenatorSerializer, NeulhaerangSerializer, NeulhaerangDonationSerializer


# Create your views here.



class MypageBadgeView(View):
    def get(self, request):
        member = Member.objects.get(member_email=request.session.get("member_email"))
        profile_badge = MemberBadge.objects.filter(member=member)
        if profile_badge:
            profile_badge = profile_badge.values('member','badge').annotate(badge_total=Count('id')).annotate(badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).order_by('-badge_total').first().get("badge_image")
        else:
            profile_badge = ""
        badge_temp = MemberBadge.objects.filter(member=member).values('member','badge').annotate(badge_total=Count('id')).annotate(badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).annotate(badge_id = F("badge"))
        nobadge_temp = Badge.objects.exclude(memberbadge__member = member).distinct()
        badge_count = MemberBadge.objects.filter(member=member).values('member','badge').annotate(badge_total=Count('id')).count()

        context = {
            'profile_image': member.profile_image,
            'member_nickname': member.member_nickname,
            'member_email': member.member_email,
            'member_age': member.member_age,
            'member_gender':member.member_gender,
            'member': member,
            'member_profile_badge': profile_badge,
            'donation_level': member.donation_level,
            'www_badge_list': badge_temp,
            'www_nobadge_list': nobadge_temp,
            'badge_count': badge_count,
            'modal_badge_name': Badge.badge_name,
        }

        return render(request, 'mypage/mypage-badge.html', context)


class MypageByeoljjiView(View):
    def get(self,request):

        member_email = request.session.get('member_email')

        if member_email:
            try:
                member = Member.objects.get(member_email=member_email)

                profile_badge = MemberBadge.objects.filter(member=member)
                if profile_badge:
                    profile_badge = profile_badge.values('member', 'badge').annotate(badge_total=Count('id')).annotate(
                        badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).order_by(
                        '-badge_total').first().get("badge_image")

                else:
                    profile_badge = ''
                byeoljji_count = MemberByeoljji.objects.filter(member=member).count()

                context = {
                    'member_nickname': member.member_nickname,
                    'donation_level': member.donation_level,
                    'member_profile_image': member.profile_image,
                    'member_profile_badge': profile_badge,
                    'donation_status': member.donation_status,
                    'total_donation_fund': member.total_donation_fund,
                    'total_donation_count': member.total_donation_count,
                    'member': member,
                    'byeoljji_count':byeoljji_count,

                }

                return render(request, 'mypage/mypage-byeoljji.html', context)

            except Member.DoesNotExist:
                # 멤버가 존재하지 않는 경우 처리
                pass

        # 멤버 이메일이 세션에 존재하지 않거나 오류 발생 시
        return HttpResponse('잘못된 요청입니다.')


class MypageDonateView(View):

    def get(self, request):
        # 세션에서 멤버 이메일을 가져옵니다.
        member_email = request.session.get('member_email')

        if member_email:
            try:
                member = Member.objects.get(member_email=member_email)

                profile_badge = MemberBadge.objects.filter(member=member)
                if profile_badge:
                    profile_badge = profile_badge.values('member','badge').annotate(badge_total=Count('id')).annotate(badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).order_by('-badge_total').first().get("badge_image")

                else :
                    profile_badge=''
                print(profile_badge)


                donation_temp = NeulhaerangDonation.objects.filter(member=member)[0:20]
                context = {
                    'www_donation_list': donation_temp,
                    'member_nickname': member.member_nickname,
                    'donation_level': member.donation_level,
                    'member_profile_image': member.profile_image,
                    'member_profile_badge': profile_badge,
                    'donation_status': member.donation_status,
                    'total_donation_fund': member.total_donation_fund,
                    'total_donation_count': member.total_donation_count,
                    'member':member,

                }

                return render(request, 'mypage/mypage-donate.html', context)

            except Member.DoesNotExist:
                # 멤버가 존재하지 않는 경우 처리
                pass

        # 멤버 이메일이 세션에 존재하지 않거나 오류 발생 시
        return HttpResponse('잘못된 요청입니다.')





    # def get(self, request):
    #     member = Member.objects.get(member_email=request.session['member_email'])
    #
    #     profile_badge = MemberBadge.objects.filter(member_id=1)[0:1].get().badge.badge_image
    #     print(request.session.get("member_email"))
    #     context = {
    #         #'www_neulhaerang_title': temp,
    #         'member_nickname': member.member_nickname,
    #         'donation_level': member.donation_level,
    #         'member_profile_image': member.profile_image,
    #         'member_profile_badge':  profile_badge,
    #         'donation_status': member.donation_status,
    #         'total_donation_fund': member.total_donation_fund,
    #         'total_donation_count': member.total_donation_count,
    #     }
    #     return render(request, 'mypage/mypage-donate.html', context)


# class MypageMainDeleteView(View):
#     def get(self, request, review_reply_id):
#         NeulhaerangReviewReply.objects.get(id=review_reply_id).delete(id=9)
#         return redirect('neulhaerang_review:review/list')




class MypageMainView(View):
    def get(self,request):
        return render(request, 'mypage/mypage-main.html')

    # def get(self, request):
    #     member = Member.objects.get(id=1)
    #     neulhaerang = Neulhaerang.objects.get(id=1)
    #
    #     member.total_donation_fund = '{:,}'.format(member.total_donation_fund)
    #     member.total_donation_count = '{:,}'.format(member.total_donation_count)
    #     # neulhaerang_review = NeulhaerangReview.objects.get(id=1)
    #     # review_title = neulhaerang_review_reply.neulhaerang_review.neulhaerang_review_title
    #
    #     profile_badge = MemberBadge.objects.filter(member_id=1)[0:1].get().badge.badge_image
    #
    #     temp = Neulhaerang.objects.filter(member_id=1)[0:2]
    #     # temp = Neulhaerang.objects.filter(member__member_email = request.session['member_email'])[0:2]
    #     neulhajang_temp = Neulhajang.objects.filter(member_id=1)[0:2]
    #     reply_temp = NeulhaerangReviewReply.objects.filter(member_id=1)[0:2]
    #     badge_temp = MemberBadge.objects.filter(member_id=1)[0:5]
    #     byeoljji_temp = MemberByeoljji.objects.filter(member_id=1)[0:4]
    #     # print(abcd[i]['neulh'])
    #     # temp.append(abcd.neulhaerang_title)
    #
    #     neulhaerang_count = Neulhaerang.objects.filter(member_id=1).count()
    #     neulhajang_count = Neulhajang.objects.filter(member_id=1).count()
    #     reply_neulhaerang = NeulhaerangReply.objects.filter(member_id=1).count()
    #     reply_neulhaerang_review = NeulhaerangReviewReply.objects.filter(member_id=1).count()
    #     byeoljji_count = MemberByeoljji.objects.filter(member_id=1).count()
    #     badge_count = MemberBadge.objects.filter(member_id=1).count()
    #
    #     total_reply = (reply_neulhaerang + reply_neulhaerang_review)
    #
    #
    #     context = {
    #                # 회원 정보
    #                'www_neulhaerang': temp,
    #                'www_neulhajang': neulhajang_temp,
    #                'member_nickname': member.member_nickname,
    #                'donation_level': member.donation_level,
    #                'member_profile_image': member.profile_image,
    #                'member_profile_badge': profile_badge,
    #                'donation_status': member.donation_status,
    #                'total_donation_fund': member.total_donation_fund,
    #                'total_donation_count': member.total_donation_count,
    #
    #                # 내가 참여한 늘해랑 게시글
    #
    #                'volunteer_duration_start_date': neulhaerang.volunteer_duration_start_date,
    #                'member_neulhaerang_count': neulhaerang_count,
    #                'member_neulhajang_count': neulhajang_count,
    #                # 'member_neulhaerang_img': neulhaerang.thumbnail_image,
    #                # 댓글 총 갯수 여기부터 하면됌 댓글, 리뷰 때려넣어놨음
    #                'member_reply_count': total_reply,
    #                # 'member_reply_review_content': reply_temp,
    #                'www_reply_content': reply_temp,
    #                # 'reply_title': review_title,
    #
    #                # 뱃지
    #                'www_badge_content': badge_temp,
    #                'www_byeoljji_content': byeoljji_temp,
    #                'byeoljji_count': byeoljji_count,
    #                'badge_count': badge_count,
    #
    #                }
    #     return render(request, 'mypage/mypage-main.html', context)


    def get(self, request):
        member_email = request.session.get('member_email')
        if member_email:
            member = get_object_or_404(Member, member_email=member_email)


            neulhaerang = Neulhaerang.objects.filter(member=member)

            member.total_donation_fund = '{:,}'.format(member.total_donation_fund)
            member.total_donation_count = '{:,}'.format(member.total_donation_count)

            profile_badge = MemberBadge.objects.filter(member=member)
            if profile_badge:
                profile_badge = profile_badge.values('member', 'badge').annotate(badge_total=Count('id')).annotate(
                    badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).order_by(
                    '-badge_total').first().get("badge_image")
            else:
                profile_badge=''


            feeds = NeulhajangAuthenticationFeed.objects.filter(member=member)
            feeds_count = feeds.count()
            feeds = feeds[0:2]




            temp = Neulhaerang.objects.filter(member=member)[0:2]
            neulhajang_temp = Neulhajang.objects.filter(member=member)[0:2]
            reply_temp = NeulhaerangReviewReply.objects.filter(member=member)[0:2]
            byeoljji_temp = MemberByeoljji.objects.filter(member=member)[0:4]

            neulhaerang_count = Neulhaerang.objects.filter(member=member).count()
            neulhajang_count = Neulhajang.objects.filter(member=member).count()
            byeoljji_count = MemberByeoljji.objects.filter(member=member).count()

            badge_temp = MemberBadge.objects.filter(member=member).values('member', 'badge').annotate(
                badge_total=Count('id')).annotate(badge_name=F("badge__badge_name")).annotate(
                badge_image=F("badge__badge_image")).annotate(badge_id = F("badge"))
            nobadge_temp = Badge.objects.exclude(memberbadge__member=member).distinct()
            badge_count = MemberBadge.objects.filter(member=member).values('member', 'badge').annotate(
                badge_total=Count('id')).count()
            reply_neulhaerang = NeulhaerangReply.objects.filter(member=member,donation__isnull=True).annotate(type = Value("늘해랑")).annotate(like_count=Count("replylike"))
            reply_neulhaerang_review = NeulhaerangReviewReply.objects.filter(member=member).annotate(type=Value("후기")).annotate(like_count=Count("reviewreplylike"))

            total_reply = list(reply_neulhaerang) + list(reply_neulhaerang_review)
            total_reply_sorted = sorted(total_reply, key=lambda item: item.created_date)
            total_reply_sorted.reverse()

            print(total_reply_sorted)
            total_reply_count = (reply_neulhaerang.count() + reply_neulhaerang_review.count())
            print(total_reply_count)


            context = {
                       # 회원 정보
                       'www_neulhaerang': temp,
                       'www_neulhajang': neulhajang_temp,
                       'member_nickname': member.member_nickname,
                       'donation_level': member.donation_level,
                       'member_profile_image': member.profile_image,
                       'member_profile_badge': profile_badge,
                       'donation_status': member.donation_status,
                       'total_donation_fund': member.total_donation_fund,
                       'total_donation_count': member.total_donation_count,
                       'member':member,
                       'neulhaerang':neulhaerang,


                       # 내가 참여한 늘해랑 게시글

                       'volunteer_duration_start_date': Neulhaerang.volunteer_duration_start_date,
                       'member_neulhaerang_count': neulhaerang_count,
                       'member_neulhajang_count': neulhajang_count,
                       # 'member_neulhaerang_img': neulhaerang.thumbnail_image,
                       # 댓글 총 갯수 여기부터 하면됌 댓글, 리뷰 때려넣어놨음
                       'member_reply_count': total_reply,
                       # 'member_reply_review_content': reply_temp,
                       'www_reply_content': reply_temp,
                       # 'reply_title': review_title,

                       # 뱃지
                       'www_byeoljji_content': byeoljji_temp,
                       'byeoljji_count': byeoljji_count,


                        'www_badge_list': badge_temp[0:5],
                        'www_nobadge_list': nobadge_temp,
                        'badge_count': badge_count,



                        'feeds':feeds,
                        'feeds_count':feeds_count,
                        'total_reply_sorted':total_reply_sorted[:2],
                        "total_reply_count" : total_reply_count,

                       }
            return render(request, 'mypage/mypage-main.html', context)


class MypageOthersLinkView(View):
    def get(self,request):
        return render(request, 'mypage/mypage-otherslink.html')


class MypagePostListView(View):
    def get(self, request):
        member = Member.objects.get(member_email=request.session['member_email'])
        neulhaerang = Neulhaerang.objects.filter(member=member)
        member_neulhaerang_count =Neulhaerang.objects.filter(member=member).count()
        profile_badge = MemberBadge.objects.filter(member=member)
        if profile_badge:
            profile_badge = profile_badge.values('member','badge').annotate(badge_total=Count('id')).annotate(badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).order_by('-badge_total').first().get("badge_image")
        else:
            profile_badge=''

        feeds = NeulhajangAuthenticationFeed.objects.filter(member=member)
        feeds_count = feeds.count()





        context = {
            'member_level': member.donation_level,
            'profile_image': member.profile_image,
            'member_nickname': member.member_nickname,
            'member_email': member.member_email,
            'member_age': member.member_age,
            'member_gender':member.member_gender,
            'member': member,
            'neulhaerang':neulhaerang,
            'member_nuelhaerang_count':member_neulhaerang_count,
            'member_profile_badge':profile_badge,
            'feeds_count':feeds_count,

        }
        return render(request, 'mypage/mypage-post-list.html',context)



class MypageProfileView(View):

    def get(self, request):
        member = Member.objects.get(member_email=request.session['member_email'])
        context = {
            'profile_image': member.profile_image,
            'member_nickname': member.member_nickname,
            'member_email': member.member_email,
            'member_age': member.member_age,
            'member_gender':member.member_gender,
            'member': member,

        }


        return render(request, 'mypage/mypage-profile.html', context)

    def save_data(request):

        if request.method == 'POST':
            member_email = request.session.get('member_email')
            if member_email:
                member = get_object_or_404(Member, member_email=member_email)
                member_nickname = request.POST.get('member_nickname', '닉네임을 지정해주세요')
                member_gender = request.POST.get('genderChk')
                profile_image = request.FILES.get('profile_image')



                files = request.FILES
                x_falg = request.POST.get("xFlag")
                kakao_falg = request.POST.get("kakaoFlag")
                print(kakao_falg)
                file = files.get("profile_image")
                if file:
                    member.profile_image = file
                    member.profile_image_choice = "user"
                elif x_falg == "true":
                    member.profile_image = ''
                    member.profile_image_choice = "user"
                elif kakao_falg =="true":
                    member.profile_image = request.session.get("kakao_image_url")
                    member.profile_image_choice = "kakao"
                member.member_nickname = member_nickname

                member.member_gender = member_gender
                member.save()

                return redirect('mypage:profile')

        return JsonResponse({'error': '잘못된 요청입니다.'})




class MypageReplyView(View):
    def get(self,request):
        # 세션에서 멤버 이메일을 가져옵니다.
        member_email = request.session.get('member_email')

        if member_email:
            try:
                member = Member.objects.get(member_email=member_email)

                profile_badge = MemberBadge.objects.filter(member=member)
                if profile_badge:
                    profile_badge = profile_badge.values('member','badge').annotate(badge_total=Count('id')).annotate(badge_name=F("badge__badge_name")).annotate(badge_image=F("badge__badge_image")).order_by('-badge_total').first().get("badge_image")
                else:
                    profile_badge = ''

                request.session['profile_badge'] = profile_badge

                reply_neulhaerang = NeulhaerangReply.objects.filter(member=member, donation__isnull=True).annotate(
                    type=Value("늘해랑")).annotate(like_count=Count("replylike"))
                reply_neulhaerang_review = NeulhaerangReviewReply.objects.filter(member=member).annotate(
                    type=Value("후기")).annotate(like_count=Count("reviewreplylike"))

                total_reply = list(reply_neulhaerang) + list(reply_neulhaerang_review)
                total_reply_sorted = sorted(total_reply, key=lambda item: item.created_date)
                total_reply_sorted.reverse()

                print(total_reply_sorted)
                total_reply_count = (reply_neulhaerang.count() + reply_neulhaerang_review.count())
                print(total_reply_count)



                donation_temp = NeulhaerangDonation.objects.filter(member=member)[0:20]
                context = {
                    'www_donation_list': donation_temp,
                    'member_nickname': member.member_nickname,
                    'donation_level': member.donation_level,
                    'member_profile_image': member.profile_image,
                    'member_profile_badge': profile_badge,
                    'donation_status': member.donation_status,
                    'total_donation_fund': member.total_donation_fund,
                    'total_donation_count': member.total_donation_count,
                    'member': member,
                    'total_reply_count': total_reply_count,

                }

                return render(request, 'mypage/mypage-reply.html', context)

            except Member.DoesNotExist:
                # 멤버가 존재하지 않는 경우 처리
                pass

        # 멤버 이메일이 세션에 존재하지 않거나 오류 발생 시
        return HttpResponse('잘못된 요청입니다.')


class MypageServiceSettingView(View):
    def get(self,request):
        return render(request, 'mypage/mypage-sevice-settings.html')


class MypageSignOutView(View):
    def get(self, request):
        return render(request, 'mypage/mypage-sign-out.html')

    def post(self, request):  # POST 메서드로 요청 처리
        member_email = request.session.get('member_email')

        # 로그아웃 시 회원 모델 업데이트
        if member_email:
            try:
                member = Member.objects.get(member_email=member_email)
                member.member_status = 'DELETED'  # 또는 다른 원하는 상태로 업데이트
                member.save()
            except Member.DoesNotExist:
                pass

            # Kakao API를 사용하여 로그아웃 처리
            access_token = request.session.get('access_token')
            if access_token:
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                }
                response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)

            # 세션 비우기
            request.session.clear()

            # 로그아웃 (Django 내장 로그아웃 함수)


        # 메인 페이지로 리디렉션
        return redirect('main:main')




class MemberChangeDonationStatusAPIView(APIView):
    def get(self, request):
        member = Member.objects.get(member_email=request.session.get("member_email"))
        if member.donation_status == "공개":
            member.donation_status = "비공개"
        else:
            member.donation_status = "공개"

        member.save()
        return Response(True)

class TimeReplyTimeView(APIView):
    def get(self, request):
        return render(request, 'mypage/mypage-main.html')


class DonationListAPIView(APIView):
    def get(self, request):
        member_email = request.session.get('member_email')
        page = int(request.GET.get("page"))
        year = request.GET.get('year')

        if not year:
            neulhaerang_dontaion = NeulhaerangDonation.objects.filter(member__member_email=member_email)
        else :
            neulhaerang_dontaion = NeulhaerangDonation.objects.filter(member__member_email=member_email,created_date__year=int(year))
        print(neulhaerang_dontaion)

        pagenator = Pagenation(page=page, page_count=5, row_count=5, query_set=neulhaerang_dontaion)

        donation_list = NeulhaerangDonationSerializer(pagenator.paged_models, many=True).data
        serialized_pagenator = PagenatorSerializer(pagenator).data

        datas = {
            'donation_list':donation_list,
            'serialized_pagenator':serialized_pagenator,

        }
        return JsonResponse(datas)


class MypageGetAthenticationFeedsByPagedAPIView(APIView):
    def get(self, request):
        member_email = request.session.get('member_email')
        page = int(request.GET.get("page"))
        feeds = NeulhajangAuthenticationFeed.objects.filter(member__member_email=member_email).annotate(neulhajang_title=F('neulhajang__neulhajang_title')).values()



        pagenator = Pagenation(page=page, page_count=5, row_count=5, query_set=feeds)

        serialized_pagenator = PagenatorSerializer(pagenator).data


        datas = {
            'feeds':pagenator.paged_models,
            'serialized_pagenator':serialized_pagenator,

        }
        return Response(datas)

class MypageDeleteAthenticationFeedAPIView(APIView):
    def get(self,request):
        feed_id = request.GET.get("feed_id")
        NeulhajangAuthenticationFeed.objects.filter(id=feed_id).delete()

        return Response(True)

class MypageDeleteReplyAPIView(APIView):
    def get(self,request):
        reply_id = request.GET.get("reply_id")
        type = request.GET.get("type")

        if type=="늘해랑":
            NeulhaerangReply.objects.filter(id=reply_id).delete()
        else:
            NeulhaerangReviewReply.objects.filter(id=reply_id).delete()

        return Response(True)


class MypageGetRepliesByPagedAPIView(APIView):
    def get(self,request):
        member_email = request.session.get('member_email')
        page = int(request.GET.get("page"))

        reply_neulhaerang = NeulhaerangReply.objects.filter(member__member_email=member_email, donation__isnull=True).annotate(
            type=Value("늘해랑")).annotate(like_count=Count("replylike")).annotate(title=F("neulhaerang__neulhaerang_title")).values()
        reply_neulhaerang_review = NeulhaerangReviewReply.objects.filter(member__member_email=member_email).annotate(
            type=Value("후기")).annotate(like_count=Count("reviewreplylike")).annotate(title=F("neulhaerang_review__review_title")).values()

        total_reply = list(reply_neulhaerang) + list(reply_neulhaerang_review)
        total_reply_sorted = sorted(total_reply, key=lambda item: item.get("created_date"))
        total_reply_sorted.reverse()

        total_reply_count = (reply_neulhaerang.count() + reply_neulhaerang_review.count())

        pagenator = Pagenation(page=page, page_count=5, row_count=5, query_set=total_reply_sorted)

        serialized_pagenator = PagenatorSerializer(pagenator).data

        datas = {
            'total_reply_sorted': pagenator.paged_models,
            'serialized_pagenator': serialized_pagenator,
        }
        return Response(datas)

class MypageGetByeoljjisByPagedAPIView(APIView):
    def get(self,request):
        member_email = request.session.get('member_email')
        page = int(request.GET.get("page"))

        byeoljjis = Byeoljji.objects.filter(memberbyeoljji__member__member_email=member_email).annotate(review_id=F("neulhaerang__neulhaerangreview")).values()




        pagenator = Pagenation(page=page, page_count=5, row_count=8, query_set=byeoljjis)

        serialized_pagenator = PagenatorSerializer(pagenator).data

        datas = {
            'byeoljjis': list(pagenator.paged_models),
            'serialized_pagenator': serialized_pagenator,
        }
        return Response(datas)

class MypageGetBadgeInfoAPIView(APIView):
    def get(self,request):
        badge_id = int(request.GET.get("badge_id"))
        badge = Badge.objects.filter(id=badge_id).annotate(category_name=F("category__category_name")).values()

        datas={
            "badge":badge.first()
        }
        return JsonResponse(datas)





#작성폼


class MypageNeulhaerangWriteFormView(View):
    def get(self,request):

        return render(request,'mypage/write/neulhaerang-write.html')

    def post(self,request):
        # category = request.POST.get("category")
        # want_fund_duration = request.POST.get("fundraising_period")
        # volunteer_start_date = request.POST.get("volunteer_start_date")
        # volunteer_end_date = request.POST.get("volunteer_end_date")
        # participants_max =request.POST.get("participants_max")
        # use_plans = request.POST.getlist("use_plan")
        # plan_moneys = request.POST.getlist("plan_money")
        # plan_comment = request.POST.get("plan_comment")
        # planDetail= request.POST.get("planDetail")


        # title = request.POST.get("title")
        # thumbnail= request.FILES.get("thumbnail")

        # inner_titles = request.POST.getlist("inner_title")
        # inner_title_content_orders =request.POST.getlist("inner_title_content_order")

        # inner_contents = request.POST.getlist("inner_content")
        # inner_content_content_orders = request.POST.getlist("inner_content_content_order")


        tags = request.POST.getlist("tag")

        openchat_link = request.POST.get("openchat_link")

        byeoljji_names = request.POST.getlist("byeoljji_name")

        byeoljji_counts = request.POST.getlist("byeoljji_count")

        #포토텍스트는 무조건 순서대로 10개씩 옴
        photo_texts = request.POST.getlist("caption")
        print(photo_texts)



        inner_photo_content_orders = request.POST.getlist("inner_photo_content_order")




        files = request.FILES.getlist("inner_photo")
        for file in files:
            print(file)
            print("1")












        return redirect('/mypage/neulhaerang/write-form/')


class MypageNeulhaerangReviewWriteFormView(View):
    def get(self, request):
        return render(request, 'mypage/write/neulhaerang-review-write.html')


class MypageNeulhajangWriteFormView(View):
    def get(self, request):
        return render(request, 'mypage/write/neulhajang-write.html')









